#!/bin/bash
pkill -f pondokrejo-app-linux
sleep 2
cp /tmp/pondokrejo-app-linux-new /home/pondokrejo-peta/htdocs/peta.pondokrejo.id/pondokrejo-app-linux
chown pondokrejo-peta:pondokrejo-peta /home/pondokrejo-peta/htdocs/peta.pondokrejo.id/pondokrejo-app-linux
chmod 755 /home/pondokrejo-peta/htdocs/peta.pondokrejo.id/pondokrejo-app-linux
su - pondokrejo-peta -s /bin/bash -c "cd /home/pondokrejo-peta/htdocs/peta.pondokrejo.id && ./run.sh"
sleep 2
ps aux | grep pondokrejo-app-linux | grep -v grep

