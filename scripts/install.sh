git -v || apt install git -y || pacman -S --noconfirm git
rm -rf shuei-controller	# Ensure no existing repo
git clone https://github.com/renatoexpert/shuei-controller
mkdir -p /usr/bin/shuei-controller 
cp shuei-controller -rv /usr/bin/
echo "Executables installed with success"

pipenv --version || apt install -y python3-venv

echo "Setting up daemon..."
cp shuei-controller/systemd/shueid.service /etc/systemd/system/ 
systemctl daemon-reload 
systemctl enable shueid 
systemctl start shueid 
systemctl status shueid
echo "Daemon configured with success"
rm -rf shuei-controller	# Cleaning
