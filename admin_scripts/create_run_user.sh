# создать system user без shell и домашней директории
sudo useradd --system --no-create-home --shell /sbin/nologin jobsvc

# дать права на папку проекта (если согласен, что сервис будет владеть проектом)
sudo chown -R jobsvc:jobsvc /home/admin/jobboard
# если хочешь оставить файлы за admin, не менять владельца — пропусти chown
