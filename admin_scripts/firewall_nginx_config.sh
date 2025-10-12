# удалить доступ к 8000 (если ранее открыт)
sudo firewall-cmd --permanent --remove-port=8000/tcp
# открыть http и https
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Проверить правило
sudo firewall-cmd --list-ports
