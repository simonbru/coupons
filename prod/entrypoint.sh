#!/bin/sh

# Make sure www-data can write in logs folder,
# even when logs is bind-mounted.
chown www-data.www-data "$DEPLOY_PATH/logs"
exec "$@"
