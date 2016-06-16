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
vagrant up --provision
```

To run ros_core type the following in a terminal:
```
cd ros_core
. devel/setup.bash
roscd pkg_ros_core
roslaunch pkg_ros_core start_demo.launch
```

To run ros_web, launch ros_core and then in a new screen run:
```
python -m SimpleHTTPServer 9000
```
Then access http://localhost:9000 from your browser. You should see the ros_core turtlesim pattern being drawn in your browser.

