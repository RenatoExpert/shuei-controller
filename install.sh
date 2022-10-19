git -v || apt install git -y || pacman -S --noconfirm git
git clone https://github.com/renatoexpert/janus-controller &&\
mkdir -p /usr/bin/janusd &&\
cp */* -rv /usr/bin/janusd &&\
echo "Executables installed with success"

echo "Setting up daemon..."
cp janusd.service /etc/systemd/system/ &&\
systemctl daemon-reload &&\
systemctl enable janusd &&\
systemctl start janusd &&\
echo "Daemon configured with success"
