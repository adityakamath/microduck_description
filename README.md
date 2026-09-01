# microduck_description

[![ROS 2](https://img.shields.io/badge/ROS_2-blue?logo=ros)](https://docs.ros.org)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

> URDF and xacro description for [Microduck](https://pollen-robotics.com/microduck/) — [Pollen Robotics](https://pollen-robotics.com/)' 25 cm open-source biped that walks, sits, kicks, and learns.

<img alt="microduck-morning" src="https://github.com/user-attachments/assets/57765600-6a0d-41c6-bde2-3b3edeca08aa" />

## Package Contents

```
microduck_description/
├── launch/urdf.launch.py        — starts robot_state_publisher
├── meshes/                      — 38 STL visual meshes
└── urdf/
    ├── microduck.urdf            — pre-built standalone URDF
    ├── microduck.urdf.xacro      — main entry point
    ├── microduck.common.xacro   — materials and joint limits
    ├── microduck.links.xacro    — link definitions
    └── microduck.joints.xacro  — joint definitions
```

<img alt="Screenshot 2026-09-01 at 23 49 31" src="https://github.com/user-attachments/assets/4d58b70c-2df7-42d7-bd8e-4f4c7f6baeda" />

## Robot
25 cm tall, 14 cm wide, under 800 g — [full spec sheet](https://pollen-robotics.com/microduck/press-kit/).

The URDF models **15 actuated joints** across:
- **Legs** (10 DOF): two 5-DOF legs, each with a 3-DOF hip (yaw + roll + pitch), knee, and ankle
- **Neck/head** (4 DOF): neck pitch, head pitch, head yaw, head roll
- **Beak** (1 DOF): articulated grasping jaw

<img alt="microduck" src="https://github.com/user-attachments/assets/65f54334-32c1-42bf-88fe-c11bde0865e9" />

> The materials in this package match the **Cream** colorway (cream shells, orange trim and beak, amber accents). Microduck ships in four colorways: **Cream**, **Graphite**, **Lavender**, and **Sky**.

| Joint group | Joints |
|---|---|
| Left leg | `left_hip_yaw`, `left_hip_roll`, `left_hip_pitch`, `left_knee`, `left_ankle` |
| Right leg | `right_hip_yaw`, `right_hip_roll`, `right_hip_pitch`, `right_knee`, `right_ankle` |
| Head/neck | `neck_pitch`, `head_pitch`, `head_yaw`, `head_roll` |
| Beak | `jaw` |

## Usage

```bash
# Build
colcon build --packages-select microduck_description

# Visualize
ros2 launch microduck_description urdf.launch.py
```

> OR use the `microduck.urdf` directly in any URDF viewer

## References

- [Microduck product page](https://pollen-robotics.com/microduck/)
- [Microduck press kit](https://pollen-robotics.com/microduck/press-kit/)
- [microduck_rl](https://github.com/pollen-robotics/microduck_rl) — MuJoCo source models and RL training stack
- [Onshape CAD](https://cad.onshape.com/documents/804927696f06d877f3f1803e/w/5b75db19292e71970de02dee/e/ef6e972847fec8d82570b35e)
- [mujoco_to_urdf](https://github.com/iory/mujoco_to_urdf) — MJCF→URDF conversion tool used as reference

## License

The URDF, xacro, and launch files in this package are Apache 2.0 — see [LICENSE](LICENSE).

The STL mesh assets originate from [pollen-robotics/microduck_rl](https://github.com/pollen-robotics/microduck_rl). Per the [Microduck press kit](https://pollen-robotics.com/microduck/press-kit/), the software stack is Apache 2.0, but the mechanical and electronic design files are not covered by that statement — refer to the upstream repository for the applicable terms before redistributing the meshes.
