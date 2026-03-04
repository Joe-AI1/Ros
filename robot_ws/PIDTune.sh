#!bin/bash
ros2 service call /ired/pid/tuning ired_msgs/srv/PIDTuning "{motor: "FL", kp: 3.0, ki: 1.5, kd: 0.02}"
ros2 service call /ired/pid/tuning ired_msgs/srv/PIDTuning "{motor: "FR", kp: 5.0, ki: 1.7, kd: 0.04}"
ros2 service call /ired/pid/tuning ired_msgs/srv/PIDTuning "{motor: "RL", kp: 5.5, ki: 1.7, kd: 0.02}"
ros2 service call /ired/pid/tuning ired_msgs/srv/PIDTuning "{motor: "RR", kp: 5.0, ki: 1.7, kd: 0.04}"
echo "Success Tune"
