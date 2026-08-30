import pyvista as pv
from pathlib import Path


# =====================================================
# Path
# =====================================================

current_dir = Path(__file__).resolve().parent

stl_dir = current_dir / "STL"


# =====================================================
# Load STL
# =====================================================

files = {
    "chassis": stl_dir / "LP02.stl",

    "wheel_FL": stl_dir / "W_FL.stl",
    "wheel_FR": stl_dir / "W_FR.stl",
    "wheel_RL": stl_dir / "W_RL.stl",
    "wheel_RR": stl_dir / "W_RR.stl",
}



meshes = {}

for name, path in files.items():

    print(f"Loading {name}: {path}")

    meshes[name] = pv.read(path)



# =====================================================
# Plotter
# =====================================================

plotter = pv.Plotter(
    window_size=(1280,720)
)



# =====================================================
# Add Actors
# =====================================================


actors = {}


actors["chassis"] = plotter.add_mesh(
    meshes["chassis"],
    color="lightgray",
    smooth_shading=True
)



actors["wheel_FL"] = plotter.add_mesh(
    meshes["wheel_FL"],
    color="black",
    smooth_shading=True
)


actors["wheel_FR"] = plotter.add_mesh(
    meshes["wheel_FR"],
    color="black",
    smooth_shading=True
)


actors["wheel_RL"] = plotter.add_mesh(
    meshes["wheel_RL"],
    color="black",
    smooth_shading=True
)


actors["wheel_RR"] = plotter.add_mesh(
    meshes["wheel_RR"],
    color="black",
    smooth_shading=True
)



# =====================================================
# Display
# =====================================================

plotter.add_axes()

plotter.show_grid()

plotter.set_background("white")


plotter.camera_position = "iso"


plotter.show()