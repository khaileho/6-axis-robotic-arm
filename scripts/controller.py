from arm_interface import MegaArmBridge
import ikpy.chain
import numpy as np

# configuration for each axis
GEAR_RATIOS = [1, 1, 1, 1, 1]
MICROSTEPPING = 16
STEPS_PER_REV = 200

def get_steps_per_radian(axis_index):
    total_steps_per_rev = STEPS_PER_REV * MICROSTEPPING * GEAR_RATIOS[axis_index]
    return total_steps_per_rev / (2 * np.pi)

# load 3d-printed arm's geometry with urdf file
arm = ikpy.chain.Chain.from_urdf_file("some_arm.urdf")

# create bridge to hardware
bridge = MegaArmBridge(port='COM3')

# target coordinates in 3d space
target_pos = [0.2, 0.1, 0.1] # x, y, z in meters

# solve inverse kinematics
joint_angles = arm.inverse_kinematics(target_position) # convert target_pos to joint angles
print(f"calculated joint angles (radians): {joint_angles}")

# convert radians to stepper steps and send
steps = [
    int(angle * get_steps_per_radian(i))
    for i, angle in enumerate(joint_angles)
]
bridge.send_targets(steps)