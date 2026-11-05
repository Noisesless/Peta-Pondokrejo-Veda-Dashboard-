#!/bin/bash

# Matikan proses lama jika ada (hanya milik user ini)
pkill -f "pondokrejo-app-linux"

# Tunggu sebentar
sleep 2

# Muat variabel lingkungan dari .env jika berkas tersedia
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Fallback default port & mode
export PORT=${PORT:-5092}
export GIN_MODE=${GIN_MODE:-release}

# Jalankan aplikasi di background dengan nohup
nohup ./pondokrejo-app-linux > app.log 2>&1 &

echo "Aplikasi berhasil dijalankan di background (Port: $PORT, Mode: $GIN_MODE)."
echo "Cek log dengan perintah: tail -f app.log"
