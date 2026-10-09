# Reto-0

Repositorio del Reto 0 - Equipo 2.

---

## Cómo iniciarlo

### 1. Puesta en marcha de los servicios

Para levantar todo el entorno, entramos en el directorio `PIA/` y ejecutamos Docker Compose:

```bash
cd PIA/
docker compose up -d
```

> **Nota:** Si no tienes Docker instalado en Linux (Ubuntu/Debian), puedes instalarlo con:
> ```bash
> sudo apt update && sudo apt install docker.io docker-compose-v2
> ```

### 2. Acceso y credenciales de los servicios

Una vez levantado el entorno, cada servicio queda corriendo en su puerto correspondiente:

| Servicio | URL / Puerto | Usuario | Contraseña |
| --- | --- | --- | --- |
| **InfluxDB** | `http://localhost:8086` | `reto` | `retoinicial123` |
| **Grafana** | `http://localhost:3000` | `reto` | `retoinicial123` |
| **Node-RED** | `http://localhost:1880` | *(Acceso directo)* | *(Sin contraseña)* |

---

## Documentación de la configuración

Para configurar los contenedores hemos utilizado Docker Compose, lo que nos permite levantar y conectar todos los servicios en un mismo entorno sin necesidad de configurarlos manualmente uno por uno.

En el archivo `PIA/docker-compose.yml` definimos los servicios principales que vamos a utilizar: **InfluxDB**, **Grafana** y **Node-RED**.

### InfluxDB

En InfluxDB lo hemos configurado mediante variables de entorno para que se inicialice automáticamente con nuestra organización, bucket y credenciales de administrador:

```yaml
environment:
  DOCKER_INFLUXDB_INIT_MODE: setup
  DOCKER_INFLUXDB_INIT_USERNAME: reto
  DOCKER_INFLUXDB_INIT_PASSWORD: retoinicial123
  DOCKER_INFLUXDB_INIT_ORG: orgsomorrostro
  DOCKER_INFLUXDB_INIT_BUCKET: bucketsomorrostro
  DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: tokensomorrostro123456789
```

Datos configurados para las conexiones:
- **Organización:** `orgsomorrostro`
- **Bucket:** `bucketsomorrostro`
- **Token de admin:** `tokensomorrostro123456789`

Así ya tenemos InfluxDB corriendo directamente con nuestros valores definidos sin tener que pasar por el asistente web inicial.

### Grafana

Hemos hecho un proceso similar para tener ya un usuario administrador creado desde el arranque y tres volúmenes mapeados:

```yaml
environment:
  GF_SECURITY_ADMIN_USER: reto
  GF_SECURITY_ADMIN_PASSWORD: retoinicial123
volumes:
  - ./datos/grafana:/var/lib/grafana
  - ./grafana/provisioning:/etc/grafana/provisioning
  - ./grafana/dashboards:/var/lib/grafana/dashboards
```

Aquí tenemos 3 volúmenes porque queremos que:
- Los datos de Grafana se guarden en `./datos/grafana`.
- Las configuraciones y fuentes de datos se guarden en `./grafana/provisioning`.
- Los dashboards de Grafana se guarden en `./grafana/dashboards`.

### Node-RED

Es mucho más simple. Le configuramos la variable de entorno:

```yaml
environment:
  - NODE_RED_CREDENTIAL_SECRET=retoinicial123
```

Con esto fijamos la clave secreta con la que Node-RED cifra las credenciales de los flujos. De esta manera, cada vez que iniciamos el contenedor puede descifrar los tokens y contraseñas guardados sin problemas y sin pedirnos una clave nueva.

---

## Archivos ignorados (.gitignore)

Un punto importante del proyecto es lo que hemos metido en `.gitignore`:

```text
BDA/games_march2025_cleaned.csv
PIA/datos/
PIA/nodered/*.backup
PIA/nodered/lib/
PIA/nodered/.npm
```

- **`BDA/games_march2025_cleaned.csv`:** Es el CSV del histórico de juegos. Lo ignoramos para no subir archivos pesados al repositorio de GitHub.
- **`PIA/datos/`:** Contiene los datos persistentes que generan los contenedores (las bases de datos locales de InfluxDB y Grafana). Al ignorar esta carpeta evitamos subir datos locales de cada máquina y subimos solo los archivos de configuración.
- **Archivos de Node-RED:** Ignoramos copias de seguridad (`*.backup`), caché (`.npm`) y librerías temporales (`lib/`).

### Nota sobre `node_modules` en Node-RED

Tuvimos un tema con esto: en principio no queríamos subir la carpeta `PIA/nodered/node_modules`, pero la hemos tenido que mantener en el repositorio porque ahí viene ya instalado el complemento de InfluxDB para Node-RED (`node-red-contrib-influxdb`). De esta forma, al levantar el contenedor con Docker Compose, ya viene listo para funcionar y usar InfluxDB sin tener que entrar a instalar nada a mano.
