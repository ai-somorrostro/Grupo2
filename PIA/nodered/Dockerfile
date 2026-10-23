FROM nodered/node-red:5.0.8

RUN mkdir -p /tmp/npm && chown node-red:node-red /tmp/npm
COPY --chown=node-red:node-red package.json package-lock.json /tmp/npm/
RUN cd /tmp/npm && npm install --omit=dev --no-audit --no-fund
RUN cp -a /tmp/npm/node_modules/. /usr/src/node-red/node_modules/ && rm -rf /tmp/npm
