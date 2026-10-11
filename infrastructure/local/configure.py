#!/usr/bin/env python3
"""Generate local-only credentials. Never overwrite an existing configuration."""
from pathlib import Path
import secrets
root = Path(__file__).resolve().parent
if any((root / name).exists() for name in (".env", ".chatwoot.env")):
    raise SystemExit("Configuration already exists. Existing credentials were not changed.")
values = {key: secrets.token_hex(32) for key in (
    "DB_ROOT_PASSWORD", "FRAPPE_ADMIN_PASSWORD", "CHATWOOT_DB_PASSWORD",
    "CHATWOOT_REDIS_PASSWORD", "CHATWOOT_SECRET_KEY_BASE")}
def write_private(name, text):
    path = root / name
    with path.open("x") as output:
        path.chmod(0o600)
        output.write(text)
write_private(".env", "".join(f"{key}={value}\n" for key,value in values.items()))
write_private(".chatwoot.env", "\n".join([
    "RAILS_ENV=production", "NODE_ENV=production", "INSTALLATION_ENV=docker",
    "FRONTEND_URL=http://localhost:3000", "FORCE_SSL=false",
    "ENABLE_ACCOUNT_SIGNUP=true", "POSTGRES_HOST=chatwoot-db",
    "POSTGRES_DATABASE=chatwoot", "POSTGRES_USERNAME=chatwoot",
    f"POSTGRES_PASSWORD={values['CHATWOOT_DB_PASSWORD']}",
    f"REDIS_URL=redis://:{values['CHATWOOT_REDIS_PASSWORD']}@chatwoot-redis:6379",
    f"SECRET_KEY_BASE={values['CHATWOOT_SECRET_KEY_BASE']}",
    "RAILS_LOG_TO_STDOUT=true", "ACTIVE_STORAGE_SERVICE=local",
    "DEFAULT_LOCALE=pt_BR", ""
]))
print("Local configuration created. Credentials remain in .env; no values printed.")
