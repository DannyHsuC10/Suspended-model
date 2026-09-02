import numpy as np
from scipy.optimize import root
from dataclasses import dataclass

import matplotlib.pyplot as plt
"""
Suspension model
       |
       |  輸入：
       |  >>> cylinder displacement
       |  輸出 :
       v <<< output force
Hydraulic system
       |
       |  求解：
       |  pressure distribution
       |  hydraulic force
       |  next cylinder displacement
       v
Suspension integration
"""

@dataclass
class HydraulicCylinder:# 液壓缸
    """液壓缸體物件"""
    name: str

    area_A: float = 1
    area_B: float = 1

    stroke: float = 0.0


    def force(self,PA,PB):
    
        return PA*self.area_A-PB*self.area_B
    
    @property
    def volume_A(self):

        return self.area_A*self.stroke


    @property
    def volume_B(self):

        return self.area_B*self.stroke

# Hydraulic Node
class HydraulicNode:# 接點(用來接接頭，N通頭)
    """保持液壓唯一與體積守恆"""

    def __init__(
        self,
        name,
        ports,
        pressure=0.0
    ):

        self.name = name
        self.ports = ports
        self.pressure = pressure
        self.index=None

    def volume_row(self,unknown):
        
        row=[]


        for actuator in unknown:

            coefficient=0


            for port in self.ports:


                if port.component == actuator.cylinder:

                    coefficient += (
                        port.sign *
                        port.area
                    )


            row.append(coefficient)


        return row

    def volume_error(self):

        volume = 0

        for p in self.ports:

            volume += (
                p.sign *
                p.volume
            )

        return volume

    def pressure_error(self):
    
        error=[]

        if len(self.ports)<=1:
            return error


        p0=self.ports[0].pressure


        for port in self.ports[1:]:

            error.append(
                port.pressure-p0
            )

        return error

@dataclass
class HydraulicActuator:

    name:str

    cylinder:HydraulicCylinder

    node_A:HydraulicNode

    node_B:HydraulicNode



    def force(self):

        return self.cylinder.force(
            self.node_A.pressure,
            self.node_B.pressure
        )


    def pressure_row(self,nodes):
        
        row=np.zeros(len(nodes))

        if self.node_A in nodes:
            row[nodes.index(self.node_A)] += self.cylinder.area_A

        if self.node_B in nodes:
            row[nodes.index(self.node_B)] -= self.cylinder.area_B

        return row
    
    def update_stroke(self,stroke):
        
        self.cylinder.stroke=stroke

@dataclass
class HydraulicPort:
    """液壓缸接頭"""
    name: str
    component: object
    side: str = None
    sign: int = 1

    @property
    def area(self):

        if isinstance(
            self.component,
            HydraulicCylinder
        ):

            if self.side == "A":
                return self.component.area_A

            elif self.side == "B":
                return self.component.area_B


        else:
            return self.component.area



    @property
    def volume(self):

        if isinstance(
            self.component,
            HydraulicCylinder
        ):

            return self.area*self.component.stroke

        else:

            return self.component.volume

@dataclass
class HydraulicInput:# 輸入流體懸吊力量源頭

    name:str
    area:float = 1
    stroke:float=0.0

    @property
    def volume(self):
        return self.area*self.stroke

class HydraulicConstraintSystem:
    
    def __init__(
        self,
        actuators,
        nodes
    ):

        self.actuators=actuators
        self.nodes=nodes

    def solve_stroke_linear(
        self,
        known
    ):

        """
        known:
        {
            actuator_name:stroke
        }

        回傳未知 cylinder stroke
        """


        unknown=[]


        for actuator in self.actuators:

            if actuator.name not in known:

                unknown.append(actuator)



        A=[]
        b=[]


        for node in self.nodes:


            row=node.volume_row(
                unknown
            )


            rhs=0


            for port in node.ports:


                # 已知輸入
                if hasattr(
                    port.component,
                    "stroke"
                ):

                    if port.component not in [
                        a.cylinder
                        for a in unknown
                    ]:

                        rhs -= (
                            port.sign *
                            port.volume
                        )


            A.append(row)
            b.append(rhs)



        A=np.array(A)
        b=np.array(b)



        x=np.linalg.solve(
            A,
            b
        )



        for actuator,value in zip(
            unknown,
            x
        ):

            actuator.update_stroke(value)



        return x


    def solve_pressure_linear(
        self,
        external_force
    ):

        """
        external_force:

        {
            actuator_name:F
        }

        """

        nodes=self.nodes


        A=[]
        b=[]


        for actuator in self.actuators:


            row=actuator.pressure_row(
                nodes
            )


            A.append(row)


            b.append(
                external_force[
                    actuator.name
                ]
            )


        A=np.array(A)
        b=np.array(b)

        print([n.name for n in self.nodes])
        print(A)
        print(A.shape)
        print(np.linalg.matrix_rank(A))

        pressure=np.linalg.solve(
            A,
            b
        )


        for node,p in zip(
            nodes,
            pressure
        ):

            node.pressure=p



        return pressure
    
#==========================================================
"""
範例液壓網路

input_f >> A & B 分流 
input_r >> C & B 分流

液壓缸A:
input_f to A >>|<<(壓力 = 0) ,外力F = k_1*s_a

液壓缸C:
input_r to C >>|<<(壓力 = 0) ,外力F = k_2*s_c

液壓缸B:
input_f to B >>|<< input_r to B ,外力F = k_3*s_b
"""
# 系統架設
input_f = HydraulicInput("input_f",1,0.01)# >>擠出液體
input_f_port = HydraulicPort("input_f",input_f,1)

input_r = HydraulicInput("input_r",1,0.005)#>>擠出液體
input_r_port = HydraulicPort("input_r",input_r,1)

A = HydraulicCylinder("A")
A_front = HydraulicPort("A_front",A,"A",-1)
A_tank = HydraulicPort("A_tank",A,"B",1)

B = HydraulicCylinder("B")
B_front = HydraulicPort("B_front",B,"A",-1)
B_rear = HydraulicPort("B_rear",B,"B",-1)

C = HydraulicCylinder("C")
C_rear = HydraulicPort("C_rear",C,"A",-1)
C_tank = HydraulicPort("C_tank",C,"B",1)

#tank = HydraulicNode("tank",[],pressure=0)
tank = HydraulicNode("tank",[A_tank,C_tank],pressure=0)# 需要檢查

node_front = HydraulicNode("front",[input_f_port,A_front,B_front])
node_rear = HydraulicNode("rear",[input_r_port,B_rear,C_rear])

actuator_A=HydraulicActuator("A",A,node_front,tank)
actuator_B=HydraulicActuator("B",B,node_front,node_rear)
actuator_C=HydraulicActuator("C",C,node_rear,tank)

system=HydraulicConstraintSystem(
    [actuator_A,actuator_B,actuator_C],
    [node_front,node_rear,tank])

# teat ==================================================
# 連續測試
known = {
    "input_f":0.01,
    "input_r":0.005
}

system.solve_stroke_linear(known)
print("A: ",A.stroke)
print("B: ",B.stroke)
print("C: ",C.stroke)

k = {
    "A":1000,
    "B":2000,
    "C":1000
}

external_force = {

    "A":k["A"]*A.stroke,

    "B":k["B"]*B.stroke,

    "C":k["C"]*C.stroke

}

print("external_force: ",external_force)

pressure = system.solve_pressure_linear(
    external_force
)

print("pressure: ", pressure)
print(actuator_A.force())
print(actuator_B.force())
print(actuator_C.force())