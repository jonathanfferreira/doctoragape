FROM node:20-bookworm-slim AS node
FROM python:3.11-slim-bookworm
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && apt-get update && apt-get install -y --no-install-recommends git curl build-essential pkg-config libmariadb-dev mariadb-client redis-tools libffi-dev libssl-dev libjpeg-dev zlib1g-dev libldap2-dev libsasl2-dev \
 && rm -rf /var/lib/apt/lists/* \
 && npm install -g yarn@1.22.22 \
 && pip install --no-cache-dir frappe-bench==5.31.0 \
 && useradd -m -u 1000 -s /bin/bash frappe
COPY scripts/fetch-upstream.py /opt/agape/scripts/fetch-upstream.py
COPY infrastructure/open-source/sources.lock.json /opt/agape/infrastructure/open-source/sources.lock.json
# Download only the Frappe apps here; Chatwoot runs from its own image.
RUN python -c "import json; p='/opt/agape/infrastructure/open-source/sources.lock.json'; j=json.load(open(p)); j['sources']=[s for s in j['sources'] if s['name']!='chatwoot']; json.dump(j,open(p,'w'))" \
 && python /opt/agape/scripts/fetch-upstream.py /opt/upstream \
 && git -C /opt/upstream/frappe branch version-15 \
 && chown -R frappe:frappe /opt/upstream
USER frappe
WORKDIR /home/frappe
RUN bench init --frappe-path /opt/upstream/frappe --frappe-branch version-15 --python python3.11 --skip-assets --skip-redis-config-generation --no-procfile --no-backups frappe-bench \
 && cd frappe-bench \
 && bench get-app --skip-assets erpnext /opt/upstream/erpnext \
 && bench get-app --skip-assets healthcare /opt/upstream/healthcare \
 && bench build \
 && cp -a sites/assets /home/frappe/agape-build-assets
WORKDIR /home/frappe/frappe-bench
COPY --chown=frappe:frappe infrastructure/local/init-frappe.sh /opt/agape/init-frappe.sh
CMD ["bench","serve","--port","8000"]
