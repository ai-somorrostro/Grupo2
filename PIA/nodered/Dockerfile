FROM nodered/node-red:5.0.8

# Copiar el manifiesto de dependencias al directorio raíz de Node-RED (/usr/src/node-red)
COPY package.json .

# Instalar los nodos y dependencias directamente dentro de la imagen
RUN npm install --unsafe-perm --no-update-notifier --no-fund --only=production
