git -v || apt install git -y || pacman -S --noconfirm git
rm -rf janus-controller	# Ensure no existing repo
git clone https://github.com/renatoexpert/janus-controller
mkdir -p /usr/bin/janusd 
cp janus-controller/* -rv /usr/bin/janus-controller 
echo "Executables installed with success"

echo "Setting up daemon..."
cp janus-controller/janusd.service /etc/systemd/system/ 
systemctl daemon-reload 
systemctl enable janusd 
systemctl start janusd 
echo "Daemon configured with success"
rm -rf janus-controller	# Cleaning
