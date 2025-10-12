# Открыть порт 8000/tcp постоянно и перезагрузить правила
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# Проверить правило
sudo firewall-cmd --list-ports
