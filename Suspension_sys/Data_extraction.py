from types import SimpleNamespace
import numpy as np


# ==========================================================
# Attitude index
# ==========================================================

FRONT_ROLL = 0
REAR_ROLL  = 1
PITCH      = 2
YAW        = 3


# ==========================================================
# Quarter result
# ==========================================================

def get_quarter_result(result, wheel):
    """
    從 full result 擷取單輪 history。

    wheel:
        0 = FL
        1 = FR
        2 = RL
        3 = RR
    """

    if wheel not in (0, 1, 2, 3):
        raise ValueError("wheel must be 0, 1, 2, or 3")

    quarter = {}

    for key, value in result.items():

        value = np.asarray(value)

        # 四輪資料
        if value.ndim == 2 and value.shape[1] == 4:
            quarter[key] = value[:, wheel]

        # 其他資料直接複製
        else:
            quarter[key] = value

    return quarter


# ==========================================================
# Pitch result
# ==========================================================

def get_pitch_result(result):
    """
    將 full logger result 轉成 pitch visualizer 使用的結果。

    Attitude definition:
        theta = [front_roll, rear_roll, pitch, yaw]
    """

    pitch = {}

    # =====================================
    # Copy original result
    # =====================================

    for key, value in result.items():
        pitch[key] = np.asarray(value)

    # =====================================
    # Front / Rear derived data
    # =====================================

    # -------------------------------------
    # Sprung displacement
    # -------------------------------------

    pitch["front_zs"] = np.mean(
        pitch["zs"][:, :2],
        axis=1
    )

    pitch["rear_zs"] = np.mean(
        pitch["zs"][:, 2:],
        axis=1
    )

    # -------------------------------------
    # Unsprung displacement
    # -------------------------------------

    pitch["front_zu"] = np.mean(
        pitch["zu"][:, :2],
        axis=1
    )

    pitch["rear_zu"] = np.mean(
        pitch["zu"][:, 2:],
        axis=1
    )

    # -------------------------------------
    # Sprung velocity
    # -------------------------------------

    pitch["front_vzs"] = np.mean(
        pitch["vzs"][:, :2],
        axis=1
    )

    pitch["rear_vzs"] = np.mean(
        pitch["vzs"][:, 2:],
        axis=1
    )

    # -------------------------------------
    # Unsprung velocity
    # -------------------------------------

    pitch["front_vzu"] = np.mean(
        pitch["vzu"][:, :2],
        axis=1
    )

    pitch["rear_vzu"] = np.mean(
        pitch["vzu"][:, 2:],
        axis=1
    )

    # =====================================
    # Tire force
    # =====================================

    if "Ft" in pitch:

        pitch["front_Ft"] = np.sum(
            pitch["Ft"][:, :2],
            axis=1
        )

        pitch["rear_Ft"] = np.sum(
            pitch["Ft"][:, 2:],
            axis=1
        )

    # =====================================
    # Body motion
    # =====================================

    pitch["heave"] = pitch["s"][:, 2]

    pitch["heave_rate"] = pitch["v"][:, 2]

    # NEW:
    # theta = [front_roll, rear_roll, pitch, yaw]
    pitch["pitch"] = pitch["theta"][:, PITCH]

    pitch["pitch_rate"] = pitch["omega"][:, PITCH]

    pitch["pitch_acc"] = pitch["alpha"][:, PITCH]

    # =====================================
    # Front / Rear roll
    # =====================================

    pitch["front_roll"] = pitch["theta"][:, FRONT_ROLL]
    pitch["rear_roll"] = pitch["theta"][:, REAR_ROLL]

    pitch["front_roll_rate"] = pitch["omega"][:, FRONT_ROLL]
    pitch["rear_roll_rate"] = pitch["omega"][:, REAR_ROLL]

    # =====================================
    # Chassis twist
    # =====================================

    pitch["chassis_twist"] = (
        pitch["theta"][:, FRONT_ROLL]
        - pitch["theta"][:, REAR_ROLL]
    )

    pitch["chassis_twist_rate"] = (
        pitch["omega"][:, FRONT_ROLL]
        - pitch["omega"][:, REAR_ROLL]
    )

    pitch["chassis_twist_acc"] = (
        pitch["alpha"][:, FRONT_ROLL]
        - pitch["alpha"][:, REAR_ROLL]
    )

    # =====================================
    # Longitudinal acceleration
    # =====================================

    pitch["ax"] = pitch["a"][:, 0]

    return pitch


# ==========================================================
# Roll result
# ==========================================================

def get_roll_result(result, axle=None):
    """
    將 full logger result 轉成 roll visualizer 使用的結果。

    Parameters
    ----------
    result : dict
        SimulationLogger.result()

    axle : str or None
        None : 全車左右資料
        "F"  : 前軸 roll
        "R"  : 後軸 roll

    Returns
    -------
    roll : dict
        給 roll visualizer 使用的資料

    Attitude definition:
        theta = [front_roll, rear_roll, pitch, yaw]
    """

    roll = {}

    # =====================================
    # Copy original result
    # =====================================

    for key, value in result.items():
        roll[key] = np.asarray(value)

    # =====================================
    # Select axle
    # =====================================

    if axle is not None:
        axle = axle.upper()

    if axle == "F":

        left_idx = [0]
        right_idx = [1]

        roll_angle_idx = FRONT_ROLL

    elif axle == "R":

        left_idx = [2]
        right_idx = [3]

        roll_angle_idx = REAR_ROLL

    elif axle is None:

        # 全車：
        # 仍然保留左右輪資料
        left_idx = [0, 2]
        right_idx = [1, 3]

        roll_angle_idx = None

    else:

        raise ValueError(
            "axle must be None, 'F', or 'R'"
        )

    # =====================================
    # Suspension displacement
    # =====================================

    roll["left_zs"] = np.mean(
        roll["zs"][:, left_idx],
        axis=1
    )

    roll["right_zs"] = np.mean(
        roll["zs"][:, right_idx],
        axis=1
    )

    roll["left_zu"] = np.mean(
        roll["zu"][:, left_idx],
        axis=1
    )

    roll["right_zu"] = np.mean(
        roll["zu"][:, right_idx],
        axis=1
    )

    # =====================================
    # Suspension velocity
    # =====================================

    roll["left_vzs"] = np.mean(
        roll["vzs"][:, left_idx],
        axis=1
    )

    roll["right_vzs"] = np.mean(
        roll["vzs"][:, right_idx],
        axis=1
    )

    roll["left_vzu"] = np.mean(
        roll["vzu"][:, left_idx],
        axis=1
    )

    roll["right_vzu"] = np.mean(
        roll["vzu"][:, right_idx],
        axis=1
    )

    # =====================================
    # Tire / suspension force
    # =====================================

    if "Ft" in roll:

        roll["left_Ft"] = np.sum(
            roll["Ft"][:, left_idx],
            axis=1
        )

        roll["right_Ft"] = np.sum(
            roll["Ft"][:, right_idx],
            axis=1
        )

    # =====================================
    # Body translation
    # =====================================

    roll["heave"] = roll["s"][:, 2]

    roll["heave_rate"] = roll["v"][:, 2]

    # =====================================
    # Body roll
    # =====================================

    if axle == "F":

        roll["roll"] = roll["theta"][:, FRONT_ROLL]
        roll["roll_rate"] = roll["omega"][:, FRONT_ROLL]
        roll["roll_acc"] = roll["alpha"][:, FRONT_ROLL]

    elif axle == "R":

        roll["roll"] = roll["theta"][:, REAR_ROLL]
        roll["roll_rate"] = roll["omega"][:, REAR_ROLL]
        roll["roll_acc"] = roll["alpha"][:, REAR_ROLL]

    else:

        # 沒有單一的「全車 roll DOF」
        #
        # 因為現在前後 roll 是獨立自由度。
        # 因此直接提供 front / rear，
        # 不強行把兩者平均成一個 roll。

        roll["front_roll"] = roll["theta"][:, FRONT_ROLL]
        roll["rear_roll"] = roll["theta"][:, REAR_ROLL]

        roll["front_roll_rate"] = roll["omega"][:, FRONT_ROLL]
        roll["rear_roll_rate"] = roll["omega"][:, REAR_ROLL]

        roll["front_roll_acc"] = roll["alpha"][:, FRONT_ROLL]
        roll["rear_roll_acc"] = roll["alpha"][:, REAR_ROLL]

        # 若 visualizer 仍然需要一個 roll，
        # 可以使用前後平均作為「代表性 roll」
        roll["roll"] = (
            roll["front_roll"]
            + roll["rear_roll"]
        ) / 2.0

        roll["roll_rate"] = (
            roll["front_roll_rate"]
            + roll["rear_roll_rate"]
        ) / 2.0

        roll["roll_acc"] = (
            roll["front_roll_acc"]
            + roll["rear_roll_acc"]
        ) / 2.0

    # =====================================
    # Chassis twist
    # =====================================

    roll["chassis_twist"] = (
        roll["theta"][:, FRONT_ROLL]
        - roll["theta"][:, REAR_ROLL]
    )

    roll["chassis_twist_rate"] = (
        roll["omega"][:, FRONT_ROLL]
        - roll["omega"][:, REAR_ROLL]
    )

    roll["chassis_twist_acc"] = (
        roll["alpha"][:, FRONT_ROLL]
        - roll["alpha"][:, REAR_ROLL]
    )

    # =====================================
    # Modal force
    # =====================================

    if axle == "F":

        roll["F_heave"] = roll["F_heave_f"]
        roll["F_roll"] = roll["F_roll_f"]

    elif axle == "R":

        roll["F_heave"] = roll["F_heave_r"]
        roll["F_roll"] = roll["F_roll_r"]

    else:

        # 全車模式：
        # 提供 front / rear 分開資料

        roll["F_heave_front"] = roll["F_heave_f"]
        roll["F_heave_rear"] = roll["F_heave_r"]

        roll["F_roll_front"] = roll["F_roll_f"]
        roll["F_roll_rear"] = roll["F_roll_r"]

    return roll