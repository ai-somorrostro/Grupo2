# Reto 0 — Equipo 2

## ¿Qué es este proyecto?

Este repositorio reúne un análisis de datos de Steam y un entorno para visualizar datos de una API. El análisis está en `SBD/` y el informe de visualización, en `BDA/`.

## Cómo iniciar cada parte

- **Análisis de Steam:** instala Jupyter, pandas y matplotlib (`pip install jupyter pandas matplotlib`), entra en `SBD/` y abre `steam_notebook.ipynb` en Jupyter o VS Code. El archivo `steam_data.csv` debe estar en esa carpeta.
- **Servicios de visualización:** necesitas Docker Desktop. Ábrelo y espera a que Docker esté en ejecución. Desde la raíz del repositorio, ejecuta `cd PIA` y luego `docker compose up -d`. Grafana está en `http://localhost:3000`, InfluxDB en `http://localhost:8086`, Node-RED en `http://localhost:1880` y Grafana MCP en `http://localhost:8000`. Las credenciales de Grafana e InfluxDB están definidas en `PIA/docker-compose.yml`.
- **Para el apartado BDA:** esta el doc en `BDA/Datos en gráficas (BDA).pdf`; no requiere iniciar servicios en esta carpeta pero se necesita influx y grafana funcionando, pero si cambiar el docker compose y el notebook para añadir el Gmail del usuario que va a recibir alertas y los datos de la organización y el token; ambas cosas están explicadas dentro del documento de BDA para saber en que bloques hay que realizar los cambios.

Para detener los servicios, ejecuta `docker compose down` desde `PIA/`.

## Solución de problemas

- Si Docker Compose no conecta, comprueba que Docker Desktop esté abierto y que Docker esté en ejecución.
- Si un puerto está ocupado, edita el mapeo correspondiente en `PIA/docker-compose.yml`. Cambia el número de la izquierda, que es el puerto de tu equipo, y deja intacto el de la derecha, que es el puerto del contenedor. Por ejemplo, cambia `3000:3000` por `3001:3000` para acceder a Grafana en `http://localhost:3001`. Luego, desde `PIA/`, ejecuta `docker compose up -d` de nuevo.
- Si el notebook no encuentra el CSV, ejecútalo desde `SBD/` y comprueba que `steam_data.csv` esté allí.
- Si faltan módulos al ejecutar el notebook, instala las dependencias: `pip install jupyter pandas matplotlib`.
