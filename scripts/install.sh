git -v || apt install git -y || pacman -S --noconfirm git
rm -rf janus-controller	# Ensure no existing repo
git clone https://github.com/renatoexpert/janus-controller
mkdir -p /usr/bin/janus-controller 
cp janus-controller -rv /usr/bin/
echo "Executables installed with success"

pipenv --version || apt install -y python3-venv

echo "Setting up daemon..."
cp janus-controller/systemd/janusd.service /etc/systemd/system/ 
systemctl daemon-reload 
systemctl enable janusd 
systemctl start janusd 
systemctl status janusd
echo "Daemon configured with success"
rm -rf janus-controller	# Cleaning
