#!/bin/bash
set -e

# 1. Update Nginx vhost
cp /tmp/peta.pondokrejo.id.conf /etc/nginx/sites-enabled/peta.pondokrejo.id.conf
nginx -t
systemctl reload nginx
echo "[1/4] Nginx configuration updated and reloaded successfully."

# 2. Setup .env with strict permissions
APP_DIR="/home/pondokrejo-peta/htdocs/peta.pondokrejo.id"
cp /tmp/.env.vps $APP_DIR/.env
chown pondokrejo-peta:pondokrejo-peta $APP_DIR/.env
chmod 600 $APP_DIR/.env
echo "[2/4] .env installed with chmod 600."

# 3. Setup .htaccess (Apache fallback) and updated run.sh
cp /tmp/.htaccess $APP_DIR/.htaccess
chown pondokrejo-peta:pondokrejo-peta $APP_DIR/.htaccess
chmod 644 $APP_DIR/.htaccess

cp /tmp/run.sh $APP_DIR/run.sh
chown pondokrejo-peta:pondokrejo-peta $APP_DIR/run.sh
chmod 755 $APP_DIR/run.sh
echo "[3/4] .htaccess and run.sh installed."

# 4. Update binary and restart
pkill -f pondokrejo-app-linux || true
sleep 2
cp /tmp/pondokrejo-app-linux-new $APP_DIR/pondokrejo-app-linux
chown pondokrejo-peta:pondokrejo-peta $APP_DIR/pondokrejo-app-linux
chmod 755 $APP_DIR/pondokrejo-app-linux
su - pondokrejo-peta -s /bin/bash -c "cd $APP_DIR && ./run.sh"
sleep 2
ps aux | grep pondokrejo-app-linux | grep -v grep
echo "[4/4] pondokrejo-app-linux restarted successfully."

