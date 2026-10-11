#!/bin/bash
set -euo pipefail
: "${DB_ROOT_PASSWORD:?Missing local database password}"
: "${FRAPPE_ADMIN_PASSWORD:?Missing local administrator password}"
# Configuration is limited to this Compose project's development volume.
mkdir -p sites/assets
cp -a /home/frappe/agape-build-assets/. sites/assets/
ls -1 apps > sites/apps.txt
bench set-config -g db_host mariadb
bench set-config -gp db_port 3306
bench set-config -g redis_cache redis://frappe-cache:6379
bench set-config -g redis_queue redis://frappe-queue:6379
bench set-config -g redis_socketio redis://frappe-queue:6379
bench set-config -gp socketio_port 9000
if [ ! -f sites/agape.localhost/site_config.json ]; then
  bench new-site agape.localhost --mariadb-user-host-login-scope "%" --mariadb-root-username root --mariadb-root-password "$DB_ROOT_PASSWORD" --admin-password "$FRAPPE_ADMIN_PASSWORD"
fi
bench --site agape.localhost list-apps | grep -q '^erpnext' || bench --site agape.localhost install-app erpnext
bench --site agape.localhost list-apps | grep -q '^healthcare' || bench --site agape.localhost install-app healthcare
bench use agape.localhost
bench --site agape.localhost list-apps
