#!/usr/bin/env bash
set -eo pipefail
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
source "$REPO_ROOT/starter_ws/.venv/bin/activate"
source "$REPO_ROOT/starter_ws/install/setup.bash"
source "$REPO_ROOT/controller_ws/install/setup.bash"
exec ros2 run team_controller controller "$@"
