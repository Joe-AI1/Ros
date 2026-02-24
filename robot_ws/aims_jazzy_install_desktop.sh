#!/bin/bash

# Exit on any error
set -e

# Countdown function
countdown() {
    echo "🚀 ROS 2 Jazzy installation will begin shortly..."
    echo "👉 Press Enter to start immediately or Ctrl+C to cancel."
    
    for i in {10..1}; do
        echo -ne "⏳ Starting in $i seconds... \r"
        read -t 1 -n 1 key && break
    done
    echo -e "\n🔧 Starting installation..."
}

countdown

echo "🔧 Checking and setting locale to UTF-8..."
locale  # check current locale

sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify new locale settings

echo "📦 Installing software-properties-common and enabling universe repo..."
sudo apt install -y software-properties-common
sudo add-apt-repository universe

echo "🌐 Installing curl..."
sudo apt update && sudo apt install -y curl

echo "🔑 Adding ROS 2 GPG key..."
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "📋 Adding ROS 2 Jazzy repository..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

echo "📥 Updating and installing ROS 2 Jazzy..."
sudo apt update
sudo apt install -y ros-dev-tools ros-jazzy-desktop

echo "🔁 Setting up environment sourcing..."
echo "source /opt/ros/jazzy/setup.bash" >> ~/ros_environment.bash
echo "source \$HOME/ros_environment.bash" >> ~/.bashrc

echo "✅ ROS 2 Jazzy installation complete."
echo "💡 Run 'source ~/.bashrc' or restart your terminal to apply changes."
