# main.py
import wheel
import Four_wheel_load as load
from Pacejka_MF_model.model import api as tire
import Vehicle_parameters as vp
tir_params = tire.load_tir("FSAE_43075R20.tir")

SL_list = [0.05]*4
car = vp.Car()




FZ_list = load.solve_suspension(ax, ay, car, check=True, F_add=None, CF_rela=None)

Fx, Fy, Fz, Mx, RRT, Mz = wheel.Four_wheel_output(FZ_list, SA_list, SL_list, tir_params, IA_list = None, P_list = None, V_list = None, Ro_list = None, check = False, sumdata=False)

