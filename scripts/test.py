import os
import ikpy.chain
import matplotlib.pyplot as plt

# fixed - false
# movable - true
active_links_mask = [False, True, True, True, True, True]
base_dir = os.path.dirname(os.path.abspath(__file__))
urdf_path = os.path.join(base_dir, "robotic-arm-model", "collision-model.urdf")
arm = ikpy.chain.Chain.from_urdf_file(urdf_path, active_links_mask=active_links_mask)
print(f"robot chain loaded: {arm.name}")
print(f"number of links: {len(arm.links)}")

print("kinematic chain structure")
for i, link in enumerate(arm.links):
    print(f"link {i}: {link.name}")


fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

# test pose
test_angles = [0] * len(arm.links)

#test_angles[2] = 1.57 # move link 2 90 degrees

real_frame = arm.forward_kinematics(test_angles)
print(f"End Effector Position (X, Y, Z): \n{real_frame[:3, 3]}")

# plot arm
arm.plot(test_angles, ax)
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)
ax.set_zlim(0, 0.2)

plt.show()