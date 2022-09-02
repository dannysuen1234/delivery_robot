#!/usr/bin/env bash

source /home/vtl/multi_floor_nav/devel/setup.bash

roslaunch magni_nav hector_mapping.launch &
roslaunch magni_nav move_base.xml &

rviz -d $(rospack find magni_nav)/rviz/navigation.rviz &
