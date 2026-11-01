# Corrected Levine practice package — 2026-11-01

Read this file for autonomous driving; the original README describes the
upstream competition starter and PS5 workflow.

## First setup after extracting on a new machine

Use Ubuntu 24.04 x86_64 with ROS 2 Jazzy Desktop. Install prerequisites using
`docs/INSTALL.md` if needed. Open a terminal in the extracted folder:

```bash
bash scripts/setup_workspace.sh
source /opt/ros/jazzy/setup.bash
source starter_ws/.venv/bin/activate
source starter_ws/install/setup.bash
cd controller_ws
python /usr/bin/colcon build --symlink-install
cd ..
```

Setup downloads the upstream simulator revisions and installs dependencies;
internet access and possibly sudo are required. The ZIP excludes external
simulator clones, virtual environments, build/install/log directories, and
machine-specific settings. Build after extraction rather than copying binaries.

## Run

From the extracted folder, terminal 1:

```bash
env -u GTK_PATH -u GIO_MODULE_DIR bash scripts/launch_sim.sh
```

Wait for RViz to show the car and map. From the same folder, terminal 2:

```bash
bash scripts/smoke_test.sh
bash scripts/launch_autonomous.sh
```

The default controller follows `levine_centerline.csv` with Pure Pursuit using
odometry. LiDAR provides forward obstacle stopping. Its requested speed is
capped at 1 m/s, with reduced speed on turns. It stops on stale sensor data
or excessive deviation from the centerline. It needs no PS5 controller.

Press Ctrl+C in terminal 2 to stop the controller. To stop the entire simulator
and RViz, run this from the extracted folder in another terminal:

```bash
bash scripts/stop_sim.sh
```

Restart both launch commands after stopping to reset the simulation.
Run only one simulator and one driving controller at a time.

## Correction and verification

The initial reactive controller could drive straight through an open map spur.
The corrected default follows the official Levine centerline instead. The
reactive `gap` mode is retained for experiments and is not the default.

In the local test, the corrected controller completed one timed lap with zero
recorded collisions and maximum sampled centerline deviation of about 0.29 m.
This is a single practice run, not validation across all competition stages.
The supplied centerline is specific to Levine; do not use this known-map
controller for the hidden-track stage or a different map without adaptation.

The original simulator, map, and scoring source were not modified. Controller
source and instructions are in `controller_ws/`; helper launch and stop scripts
are in `scripts/`.

## Attribution

Competition starter: https://github.com/KayiiX/CIE-KFUPM-F1tenth-Autonomous-Racing-Competition

Preserve upstream notices in `THIRD_PARTY_NOTICES.md`. The separate controller
implements the established Pure Pursuit algorithm with the supplied Levine
centerline and was developed with AI assistance. Follow your competition's
and university's attribution and AI disclosure requirements.
