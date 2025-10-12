sudo mkdir -p /etc/ssl/jobboard
sudo openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -subj "/C=US/ST=State/L=City/O=Org/CN=job.lab" \
  -keyout /etc/ssl/jobboard/jobboard.key \
  -out /etc/ssl/jobboard/jobboard.crt
sudo chown root:root /etc/ssl/jobboard/* && sudo chmod 640 /etc/ssl/jobboard/*
