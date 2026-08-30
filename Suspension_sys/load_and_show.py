import sys
from pathlib import Path
from data_visualization.Simulation_Logger import SimulationLogger
from data_visualization.Dynamic_Visualizer_dashboard import SuspensionDashboard

current_dir = Path(__file__).resolve().parent

"""
之前有改格式data需要重新建立
"""

result_file = current_dir/ "data.pkl"

# =====================================================
# Load simulation result

logger = SimulationLogger.load(result_file)
result = logger.result()

# Quick check
print("Loaded result:")
for key, value in result.items():
    print(
        f"{key}: shape={value.shape}")


# =====================================================
# Visualization

viewer = SuspensionDashboard(result)

viewer.show()

