######################################################################################################
# FEDORA 35 KICKSTART configuration file
#
# https://docs.fedoraproject.org/en-US/fedora/f35/install-guide/appendixes/Kickstart_Syntax_Reference/
#
# Validate on fedora with
#   $ sudo dnf install pykickstart
#   $ ksvalidator /path/to/kickstart.ks
######################################################################################################

# Add additional repos
url --mirrorlist="https://mirrors.fedoraproject.org/metalink?repo=fedora-35&arch=x86_64"
repo --name=fedora-updates --mirrorlist="https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f35&arch=x86_64" --cost=0
repo --name=rpmfusion-free --mirrorlist="https://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-35&arch=x86_64" --includepkgs=rpmfusion-free-release
repo --name=rpmfusion-free-updates --mirrorlist="https://mirrors.rpmfusion.org/mirrorlist?repo=free-fedora-updates-released-35&arch=x86_64" --cost=0
repo --name=rpmfusion-nonfree --mirrorlist="https://mirrors.rpmfusion.org/mirrorlist?repo=nonfree-fedora-35&arch=x86_64" --includepkgs=rpmfusion-nonfree-release
repo --name=rpmfusion-nonfree-updates --mirrorlist="https://mirrors.rpmfusion.org/mirrorlist?repo=nonfree-fedora-updates-released-35&arch=x86_64" --cost=0

bootloader --location=mbr --driveorder=sda --append="nomodeset rhgb quiet"

# Localisation
keyboard --vckeymap=gb --xlayouts='gb'
lang en_GB.UTF-8
timezone Europe/London --utc

# Disks
autopart --type=btrfs
ignoredisk --only-use=sda
clearpart --none --initlabel

# Network information
network  --bootproto=dhcp --device=eth0 --ipv6=auto --activate
network  --hostname=$hostname

# Users
# Disable root
rootpw --lock
user --groups=wheel --name=$username --password=$userpass --plaintext --gecos="$username"

selinux --permissive

# Use CDROM installation media
cdrom

# Enable firewall and open SSH
firewall --enabled --service=ssh

# Run the Setup Agent on first boot
firstboot --enable

# Text mode install
text

# ansible, neovim
%packages
@^server-product-environment
@container-management
@guest-agents

%end

# Start of the %post section with logging into /root/ks-post.log
%post --log=/root/ks-post.log

# Add docker repo
dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install my standard packages
dnf update -y
dnf install ansible neovim git docker-ce docker-ce-cli containerd.io -y

# Configure docker
sudo groupadd docker
sudo usermod -aG docker $username
systemctl enable docker.service
systemctl enable containerd.service
%end

# Reboot After Installation
reboot --eject