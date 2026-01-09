#!/usr/bin/env python3
from controller import Robot, Motor
import sys
import math
import csv


# INICIALIZAÇÃO
robot = Robot()

# devices = robot.getDevice()

# print("=== Devices disponíveis ===")
# for d in devices:
    # print(d)
    
TIME_STEP = int(robot.getBasicTimeStep())
T_s = TIME_STEP / 1000.0

# MOTORES
motor_names = ["m1_motor", "m2_motor", "m3_motor", "m4_motor"]


motors = []
for name in motor_names:
    m = robot.getDevice(name)
    m.setPosition(float('inf'))
    m.setVelocity(0.0)
    motors.append(m)

gps = robot.getDevice("gps")
gps.enable(TIME_STEP)



# Log de dados
file = open("log_siso.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["t", "w", "z"])

t = 0.0

# Parâmetros do teste
w = 150.0  # velocidade das hélices (ajuste fino pode ser necessário)
t_ramp = 6  # segundos até elevar o drone
t_sim = 6   # duração da simulação


# LOOP PRINCIPAL
while robot.step(TIME_STEP) != -1:
    t = robot.getTime()
    # Simple SISO input (rampa)
    if t < t_ramp:
        w_in = (t / t_ramp) * w
    else:
        w_in = w
    
    # Aplica w1=w2=w3=w4=w
    # for m in motors:
        # m.setVelocity(w_in)
    motors[0].setVelocity(-w_in)    # m1
    motors[1].setVelocity(w_in)   # m2
    motors[2].setVelocity(-w_in)    # m3
    motors[3].setVelocity(w_in)   # m4
    # Mede altitude
    gps_values = gps.getValues()
    z = gps_values[2]  # eixo vertical
    
    
    # Salva
    writer.writerow([t, w_in, z])
    
    if t > t_sim:
        break
        
    # SEU DEBUG
    print(f"t[k]:{t:.1f} | w[k]:{w_in:.1f} | z[k]:{z:.3f}")
    




print("Arquivo log_resposta_sistema.csv salvo com sucesso.")
file.close()


        