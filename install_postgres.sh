dnf update -y
dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf install -y postgresql17-server postgresql17-contrib
/usr/pgsql-17/bin/postgresql-17-setup initdb
systemctl enable postgresql-17 --now
sudo -u postgres psql -c "CREATE USER jobuser WITH PASSWORD 'jobpass';"
sudo -u postgres psql -c "CREATE DATABASE jobboard OWNER jobuser;"
systemctl restart postgresql-17.service