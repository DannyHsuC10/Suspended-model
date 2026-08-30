import numpy as np
from scipy.optimize import root
from dataclasses import dataclass

import matplotlib.pyplot as plt
"""
範例問題

input_f >> A & B 分流 
input_r >> C & B 分流

液壓缸A:
input_f to A >>|<<(壓力 = 0) ,外力F = k_1*s_a

液壓缸C:
input_r to C >>|<<(壓力 = 0) ,外力F = k_2*s_c

液壓缸B:
input_f to B >>|<< input_r to B ,外力F = k_3*s_b
"""



@dataclass
class HydraulicCylinder:# 液壓缸

    name: str

    area_A: float
    area_B: float

    stroke: float = 0.0


    def force(self, PA, PB):

        return (
            PA*self.area_A
            -
            PB*self.area_B
        )


    @property
    def volume_A(self):

        return self.area_A*self.stroke


    @property
    def volume_B(self):

        return self.area_B*self.stroke

@dataclass
class Spring:

    k: float
    displacement: float = 0.0


    @property
    def force(self):

        return self.k*self.displacement

# Hydraulic Node
class HydraulicNode:# 接點(用來接接頭，N通頭)
    

    def __init__(
        self,
        name,
        ports,
        pressure=0.0
    ):

        self.name = name
        self.ports = ports
        self.pressure = pressure


    def volume_error(self):

        volume = 0

        for p in self.ports:

            volume += (
                p.sign *
                p.volume
            )

        return volume

@dataclass
class HydraulicActuator:


    name:str

    cylinder:HydraulicCylinder

    spring:Spring

    node_A:HydraulicNode

    node_B:HydraulicNode


    def update_stroke(self,stroke):

        self.cylinder.stroke = stroke
        self.spring.displacement = stroke



    def pressure_force_error(self):

        Fhyd = self.cylinder.force(
            self.node_A.pressure,
            self.node_B.pressure
        )


        return (
            Fhyd -
            self.spring.force
        )

@dataclass
class HydraulicPort:# 接頭
    name: str
    component: object
    side: str = None
    sign: int = 1


    @property
    def volume(self):

        if isinstance(self.component, HydraulicCylinder):

            if self.side == "A":
                return self.component.volume_A

            elif self.side == "B":
                return self.component.volume_B

        else:
            return self.component.volume

@dataclass
class HydraulicInput:# 輸入流體懸吊力量源頭

    name:str
    area:float
    stroke:float=0.0

    @property
    def volume(self):
        return self.area*self.stroke

#==========================================================
A = HydraulicCylinder("A",1,1)
B = HydraulicCylinder("B",1,1)
C = HydraulicCylinder("C",1,1)

spring_A = Spring(1000)
spring_B = Spring(2000)
spring_C = Spring(1000)

input_f = HydraulicInput("input_f",1.0,0.01)
input_r = HydraulicInput("input_r",1.0,0.005)

tank = HydraulicNode("tank",[],pressure=0)

A_front = HydraulicPort("A_front",A,"A",-1)
A_tank = HydraulicPort("A_tank",A,"B",1)

B_front = HydraulicPort("B_front",B,"A",-1)
B_rear = HydraulicPort("B_rear",B,"B",-1)

C_rear = HydraulicPort("C_rear",C,"A",-1)
C_tank = HydraulicPort("C_tank",C,"B",1)

input_f_port = HydraulicPort("input_f",input_f,1)
input_r_port = HydraulicPort("input_r",input_r,1)

node_front = HydraulicNode("front",[input_f_port,A_front,B_front])
node_rear = HydraulicNode("rear",[input_r_port,B_rear,C_rear])

actuator_A = HydraulicActuator("A",A,spring_A,node_front,tank)
actuator_B = HydraulicActuator("B",B,spring_B,node_front,node_rear)
actuator_C = HydraulicActuator("C",C,spring_C,node_rear,tank)


#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class HydraulicSystem:
    def __init__(self,nodes,actuators):

        self.nodes = nodes
        self.actuators = actuators

    def residual(self,x):

        sA,sB,sC,Pf,Pr = x

        # update displacement
        self.actuators[0].update_stroke(sA)
        self.actuators[1].update_stroke(sB)
        self.actuators[2].update_stroke(sC)

        # update pressure
        self.nodes[0].pressure = Pf
        self.nodes[1].pressure = Pr

        errors=[]

        # volume conservation
        for node in self.nodes:

            errors.append(node.volume_error())

        # force equilibrium
        for actuator in self.actuators:

            errors.append(actuator.pressure_force_error())

        return np.array(errors)

    def solve(self,x0):

        result = root(self.residual,x0)

        return result

# test ==========================================
# 單次測試

"""
system = HydraulicSystem(
    [
        node_front,
        node_rear
    ],
    [
        actuator_A,
        actuator_B,
        actuator_C
    ]
)

x0=[
    0.005,
    0.002,
    0.005,
    10000,
    5000
]


result = system.solve(x0)


print(result.x)

print(system.residual(result.x))


result=system.solve(x0)
print("Success:",result.success)
print("Solution:",result.x)
print("Residual:",system.residual(result.x))
"""

# teat 2 ==================================================
# 連續測試
def hydraulic_sweep(system,input_f,input_r,x0,f_range,r_range):
    
    data=[]

    for sf,sr in zip(f_range,r_range):

        input_f.stroke=sf
        input_r.stroke=sr

        result=system.solve(x0)

        x=result.x

        data.append([
            sf,
            sr,
            x[0],
            x[1],
            x[2],
            x[3],
            x[4]
        ])

    return np.array(data)

steps=50

f_range=np.linspace(
    0,
    0.05,
    steps
)

r_range=np.linspace(
    0,
    0.01,
    steps
)


x0=[
    0.001,
    0.001,
    0.001,
    1,
    1
]
system = HydraulicSystem(
    [
        node_front,
        node_rear
    ],
    [
        actuator_A,
        actuator_B,
        actuator_C
    ]
)

print(input_f.volume,input_r.volume)
print(node_front.volume_error(),node_rear.volume_error())

data=hydraulic_sweep(
    system,
    input_f,
    input_r,
    x0,
    f_range,
    r_range
)



plt.figure(figsize=(8,5))

plt.plot(data[:,0],data[:,2],label="Cylinder A")

plt.plot(data[:,0],data[:,3],label="Cylinder B")

plt.plot(data[:,0],data[:,4],label="Cylinder C")


plt.xlabel("Input front stroke (m)")
plt.ylabel("Cylinder stroke (m)")

plt.legend()
plt.grid()

plt.show()
plt.show()

plt.figure(figsize=(8,5))

plt.plot(data[:,0],data[:,5],label="Front pressure")

plt.plot(data[:,0],data[:,6],label="Rear pressure")


plt.xlabel("Input front stroke (m)")
plt.ylabel("Pressure")


plt.legend()
plt.grid()

plt.show()