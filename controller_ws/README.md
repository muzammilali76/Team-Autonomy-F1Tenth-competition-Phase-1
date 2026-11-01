# Autonomous simulator controller

This separate ROS 2 Jazzy package follows the official Levine centerline using
odometry and pure pursuit, with a default speed limit of 1 m/s and reduced
speed in turns. It subscribes to `/scan` for forward obstacle stopping and
publishes to `/drive`. It stops on stale scans/odometry, excessive centerline
deviation, or a blocked forward path. This is a known-track practice controller;
it must not be used for the hidden-track stage. No additional Python libraries
are required. The simulator provides `maps/levine_centerline.csv`.

The earlier reactive implementation remains available via `--ros-args -p
mode:=gap`, but it can follow open map spurs out of the circuit and is not the
default. The centerline mode is specific to the unmodified Levine practice map.

Run these commands from the competition repository root, with the simulator
already running. Stop any other controller first.

```bash
bash scripts/launch_autonomous.sh
```

To use a lower speed:

```bash
bash scripts/launch_autonomous.sh --ros-args -p max_speed:=0.5
```

Press Ctrl+C in the controller terminal to stop. If the controller was started
by the assistant in the background, stop it with:

```bash
pkill -INT -f '^/.*controller_ws/install/team_controller/lib/team_controller/controller( |$)'
```

Normal interruption publishes a zero-speed command before exiting. After a
forced termination, run `bash scripts/stop_car.sh` to clear the last command.

To close the entire competition simulation, including RViz:

```bash
bash scripts/stop_sim.sh
```

To rebuild after changing package metadata:

```bash
source /opt/ros/jazzy/setup.bash
source starter_ws/.venv/bin/activate
source starter_ws/install/setup.bash
cd controller_ws
python /usr/bin/colcon build --symlink-install
```

The executable is `ros2 run team_controller controller` after sourcing
`controller_ws/install/setup.bash`. The launcher sources all required
environments automatically. The accepted `max_speed` range is (0, 1.5] m/s;
the baseline algorithm currently requests at most 1 m/s.
