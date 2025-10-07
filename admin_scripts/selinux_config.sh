sudo cp /etc/selinux/config /etc/selinux/config.bak
sudo sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config