import re

# 1. Update nginx.conf
with open('/etc/nginx/nginx.conf', 'r') as f:
    conf = f.read()

target = 'limit_req_zone $binary_remote_addr zone=sidateka_api:10m rate=10r/s;'
replacement = '''limit_req_zone $binary_remote_addr zone=sidateka_api:10m rate=10r/s;
    # Pondokrejo SIG Rate Limiting & Anti-Scraping
    limit_req_zone $binary_remote_addr zone=pdrj_residents:10m rate=3r/s;
    limit_req_zone $binary_remote_addr zone=pdrj_login:10m rate=5r/m;'''

if target in conf and 'zone=pdrj_residents' not in conf:
    conf = conf.replace(target, replacement)
    with open('/etc/nginx/nginx.conf', 'w') as f:
        f.write(conf)
    print("nginx.conf updated")
else:
    print("nginx.conf already updated or target not found")

# 2. Update peta.pondokrejo.id.conf
vhost_content = '''server {
  listen 80;
  listen [::]:80;
  listen 443 quic;
  listen 443 ssl;
  listen [::]:443 quic;
  listen [::]:443 ssl;
  http2 on;
  http3 off;
  ssl_certificate_key /etc/nginx/ssl-certificates/peta.pondokrejo.id.key;
  ssl_certificate /etc/nginx/ssl-certificates/peta.pondokrejo.id.crt;
  server_name peta.pondokrejo.id;
  root /home/pondokrejo-peta/htdocs/peta.pondokrejo.id;

  access_log /home/pondokrejo-peta/logs/nginx/access.log main;
  error_log /home/pondokrejo-peta/logs/nginx/error.log;

  if ($scheme != "https") {
    rewrite ^ https://$host$request_uri permanent;
  }

  location ~ /.well-known {
    auth_basic off;
    allow all;
  }

  include /etc/nginx/global_settings;

  # Security Hardening: HSTS
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

  index index.html;

  location ~* ^/desa/upload/.*\.php$ {
    deny all;
    return 404;
  }

  # Rate limiting for residents data (Anti bulk-scraping)
  location = /residents.json {
    limit_req zone=pdrj_residents burst=5 nodelay;
    proxy_pass http://127.0.0.1:5092;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
    proxy_busy_buffers_size 256k;
  }

  # Rate limiting for login attempts (Anti brute-force)
  location = /api/login {
    limit_req zone=pdrj_login burst=3 nodelay;
    proxy_pass http://127.0.0.1:5092;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location / {
    proxy_pass http://127.0.0.1:5092/;
    proxy_pass_header Referer;
    proxy_http_version 1.1;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Server $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
    proxy_pass_request_headers on;
    proxy_max_temp_file_size 0;
    proxy_connect_timeout 900;
    proxy_send_timeout 900;
    proxy_read_timeout 900;
    proxy_buffer_size 128k;
    proxy_buffers 4 256k;
    proxy_busy_buffers_size 256k;
    proxy_temp_file_write_size 256k;
  }
}
'''

with open('/etc/nginx/sites-enabled/peta.pondokrejo.id.conf', 'w') as f:
    f.write(vhost_content)
print("peta.pondokrejo.id.conf updated")

