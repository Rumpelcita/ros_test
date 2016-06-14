#!/bin/bash

echo "Provisioning virtual machine..."
echo "Installing Git"
    apt-get install git -y
echo "Installing Android Dependencies"
   apt-get install unzip -y
   apt-get install openjdk-7-jdk -y
echo "Installing Android"
   wget https://dl.google.com/dl/android/studio/ide-zips/2.1.2.0/android-studio-ide-143.2915827-linux.zip
   unzip android-studio-ide-143.2915827-linux.zip -d ros_android
echo "Installing ROS"
   echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list
   apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net --recv-key 0xB01FA116
   apt-get update
   apt-get install ros-indigo-desktop-full -y
echo "Init rosdep"
   rosdep init
   rosdep update
   rosdep fix-permissions
   echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
   source ~/.bashrc
echo "Installing ros install"
   apt-get install python-rosinstall -y
echo "Installing turtlesim"
   apt-get install ros-indigo-turtlesim -y
echo "Installing rosbridge"
   apt-get install ros-indigo-rosbridge-server -y
echo "Installing rosjava"
   apt-get install ros-indigo-rosjava -y
echo "Installing rosandroid"
   wget https://github.com/Rumpelcita/android_core/archive/indigo.zip
   unzip indigo.zip -d ros_android 
echo "Installing roslibjs"
   wget -O /home/vagrant/ros_web/src/lib/roslib.js https://raw.githubusercontent.com/RobotWebTools/roslibjs/develop/build/roslib.js
   wget -O /home/vagrant/ros_web/src/lib/roslib.min.js https://raw.githubusercontent.com/RobotWebTools/roslibjs/develop/build/roslib.min.js
   wget -O /home/vagrant/ros_web/src/lib/eventemitter2.min.js http://cdn.robotwebtools.org/EventEmitter2/current/eventemitter2.min.js
echo "Updating locale"
update-locale LANG=C LANGUAGE=C LC_ALL=C LC_MESSAGES=POSIX
export LC_ALL="C" 
