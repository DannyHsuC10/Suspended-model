import numpy as np
import pyvista as pv
from pathlib import Path

from data_visualization.Simulation_Logger import SimulationLogger

scale = 1000

# =====================================================
# Load simulation result
# =====================================================

current_dir = Path(__file__).resolve().parent

result_file = current_dir / "data.pkl"


logger = SimulationLogger.load(result_file)
result = logger.result()


print("Loaded result:")
for key, value in result.items():
    print(f"{key}: shape={value.shape}")



# =====================================================
# Extract vehicle motion
# =====================================================

time_data = result["t"]



# =====================================================
# Vehicle body
# =====================================================

s = result["s"]

x = s[:,0]
y = s[:,1]
z = s[:,2]



theta = result["theta"]


roll = (
    theta[:,0] +
    theta[:,1]
) / 2


pitch = theta[:,2]

yaw = theta[:,3]



# =====================================================
# Wheel motion
# =====================================================


# unsprung vertical motion
zu = result["zu"]


# camber
IA = result["IA"]


# steering
steer = result["steer"]



# =====================================================
# Wheel static position
# =====================================================

# 這裡先手動設定
# 之後可以直接換成 suspension geometry


wheel_base_position = {

    "FL": (-0.8,  0.65, 0),
    "FR": (-0.8, -0.65, 0),

    "RL": ( 0.8,  0.65, 0),
    "RR": ( 0.8, -0.65, 0),
}


wheel_id = {
    "FL":0,
    "FR":1,
    "RL":2,
    "RR":3
}



# =====================================================
# Load STL
# =====================================================


stl_dir = current_dir / "STL"


chassis_mesh = pv.read(
    stl_dir / "LP02.stl"
)


wheel_mesh = {

    name:
    pv.read(stl_dir / f"W_{name}.stl")

    for name in wheel_id.keys()

}



# =====================================================
# Create Plotter
# =====================================================


plotter = pv.Plotter(
    window_size=(1280,720)
)



# chassis

car = plotter.add_mesh(
    chassis_mesh,
    color="lightgray",
    smooth_shading=True
)



# wheels

wheels = {}


for name, mesh in wheel_mesh.items():

    wheels[name] = plotter.add_mesh(
        mesh,
        color="black",
        smooth_shading=True
    )



plotter.add_axes()

plotter.show_grid()

plotter.set_background("white")

plotter.camera_position = "iso"



# =====================================================
# Animation
# =====================================================


plotter.show(
    interactive_update=True
)


frame = 0


while True:

    if frame >= len(time_data):
        frame = 0


    if frame % 50 == 0:

        print(
            "frame:", frame,
            "FL:", zu[frame,0],
            "FR:", zu[frame,1],
            "RL:", zu[frame,2],
            "RR:", zu[frame,3]
        )



    # =================================================
    # Update chassis
    # =================================================




    car.SetPosition(
        x[frame]*scale,
        y[frame]*scale,
        z[frame]*scale
    )

    car.SetOrientation(
        np.degrees(roll[frame]),
        -np.degrees(pitch[frame]),
        np.degrees(yaw[frame])
    )



    # =================================================
    # Update wheels
    # =================================================


    for name, idx in wheel_id.items():


        actor = wheels[name]


        base_x, base_y, base_z = wheel_base_position[name]


        # suspension movement
        wheel_z = base_z + zu[frame,idx]*scale


        actor.SetPosition(
            base_x + x[frame],
            base_y + y[frame],
            wheel_z + z[frame]
        )


        # steering + camber

        actor.SetOrientation(
            np.degrees(IA[frame,idx]),
            np.degrees(steer[frame,idx]),
            0
        )



    # refresh

    plotter.update()


    frame += 1