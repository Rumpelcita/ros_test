# ros_test
Implementation of different ros modules.

## Setup
To run this you will need vagrant and virtualbox. All the dependencies needed to run this project are inside the vagrant VM.

To install vagrant on a Debian base environment, open a terminal and run:
```
./first_setup.sh
```

Then provision the VM with:
```
Vagrant up --provision
```

To run roscore type the following in a terminal:
```
. devel/setup.bash
roscd pkg_ros_core
roslaunch pkg_ros_core start_demo.launch
```
