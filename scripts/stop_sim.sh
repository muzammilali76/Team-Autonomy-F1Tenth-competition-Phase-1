#!/usr/bin/env bash
set -euo pipefail
# Stop this repository's controller, then the competition ROS launch process.
# ROS launch handles shutting down its simulator, RViz, and monitor children.
pkill -INT -f '^/.*controller_ws/install/team_controller/lib/team_controller/controller( |$)' || true
pkill -INT -f '^/.*ros2 launch competition_bringup competition_sim_launch.py( |$)' || true
echo 'Sent shutdown requests to the autonomous controller and competition simulator.'
