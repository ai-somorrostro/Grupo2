import time
import numpy as np
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import timesfm

# 1. Conexión con InfluxDB
INFLUX_URL = "http://influxdb:8086"
INFLUX_TOKEN = "tokensomorrostro123456789"
INFLUX_ORG = "orgsomorrostro"
INFLUX_BUCKET = "bucketsomorrostro"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)
delete_api = client.delete_api()

# 2. Cargar modelo TimesFM (los pesos se descargan/guardan en /root/.cache/huggingface -> PIA/datos/modelo)
print("Cargando modelo TimesFM 2.5...")
modelo = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
modelo.compile(timesfm.ForecastConfig(max_context=2048, max_horizon=5024))
print("Modelo cargado y listo.")

INTERVALO_SEGUNDOS = 600  # Pasos de 10 minutos
HORIZONTE = 4176          # 4176 pasos x 10 min = 29 días (29 días exactos a futuro)

# 3. Bucle continuo de predicción
while True:
    try:
        # Leer todos los datos reales disponibles sin límite hacia atrás, agrupados cada 10 minutos
        query = f'''
        from(bucket: "{INFLUX_BUCKET}")
          |> range(start: 0)
          |> filter(fn: (r) => r["_measurement"] == "cs2_live_players")
          |> filter(fn: (r) => r["_field"] == "jugadores")
          |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)
        '''
        tablas = query_api.query(query)
        historico = [r.get_value() for t in tablas for r in t.records]

        if len(historico) >= 1:
            # Tomar todo el histórico (hasta el límite de contexto del modelo: 2048 puntos ~= 7 días)
            contexto = historico[-2048:]
            # Si hay pocos puntos (acabamos de arrancar), replicamos para que TimesFM tenga contexto mínimo
            datos_input = contexto if len(contexto) >= 3 else (contexto * 3)[:3]
            # Predecir los siguientes pasos con TimesFM (estimación puntual y cuantiles)
            pred, cuantiles = modelo.forecast(horizon=HORIZONTE, inputs=[np.array(datos_input, dtype=np.float32)])
            proyeccion = pred[0]
            q_vals = cuantiles[0]

            ahora = int(time.time())
            ahora_grid = (ahora // INTERVALO_SEGUNDOS) * INTERVALO_SEGUNDOS
            val_origen = float(historico[-1])

            # Punto de origen alineado con ancho cero (une perfectamente con el dato real)
            puntos_pred = [
                Point("cs2_prediccion")
                .field("prediccion", val_origen)
                .field("prediccion_min", val_origen)
                .field("prediccion_max", val_origen)
                .time(ahora_grid * 1_000_000_000)
            ]

            # Puntos futuros alineados a 10 min: cono de incertidumbre (cuantiles 10% y 90%)
            for i in range(HORIZONTE):
                tiempo_futuro_ns = (ahora_grid + (i + 1) * INTERVALO_SEGUNDOS) * 1_000_000_000
                v_mid = float(proyeccion[i])
                v_min = float(q_vals[i, 1])  # Percentil 10
                v_max = float(q_vals[i, 9])  # Percentil 90

                # Asegurar que el cono envuelve a la predicción central
                v_min = min(v_min, v_mid)
                v_max = max(v_max, v_mid)

                p = (
                    Point("cs2_prediccion")
                    .field("prediccion", v_mid)
                    .field("prediccion_min", v_min)
                    .field("prediccion_max", v_max)
                    .time(tiempo_futuro_ns)
                )
                puntos_pred.append(p)

            # Limpiar predicciones obsoletas para mantener solo el cono activo limpio
            delete_api.delete(
                start="1970-01-01T00:00:00Z",
                stop="2030-01-01T00:00:00Z",
                predicate='_measurement="cs2_prediccion"',
                bucket=INFLUX_BUCKET,
                org=INFLUX_ORG
            )
            write_api.write(bucket=INFLUX_BUCKET, record=puntos_pred)
            print(f"[{time.strftime('%X')}] Predicción en cono guardada en InfluxDB ({len(puntos_pred)} puntos calculados con {len(contexto)} puntos históricos de contexto).")
        else:
            print(f"[{time.strftime('%X')}] Esperando más datos reales de InfluxDB (actuales: {len(historico)})...")

    except Exception as error:
        print(f"[{time.strftime('%X')}] Error: {error}")

    time.sleep(60)
