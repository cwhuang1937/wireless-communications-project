import random
import math
import time
import matplotlib.pyplot as plt

def decide_turn(x, y, vx, vy):
     
    if x == 0 and y == 0 and vx == -1:
        vx = 0
        vy = 1
    elif x == 0 and y == 0 and vy == -1:
        vx = 1
        vy = 0
    elif x == 3000 and y == 0 and vx == 1:
        vx = 0
        vy = 1
    elif x == 3000 and y == 0 and vy == -1:
        vx = -1
        vy = 0
    elif x == 0 and y == 3000 and vx == -1:
        vx = 0
        vy = -1
    elif x == 0 and y == 3000 and vy == 1:
        vx = 1
        vy = 0
    elif x == 3000 and y == 3000 and vx == 1:
        vx = 0
        vy = -1
    elif x == 3000 and y == 3000 and vy == 1:
        vx = -1
        vy = 0
    else:
        p = random.random()
        if p >= 0.5:
            return vx, vy
        elif p >= 1/3 and p < 0.5:
            if vx == 1 and vy == 0:
                vx = 0
                vy = -1
            elif vx == 0 and vy == 1:
                vx = 1
                vy = 0
            elif vx == -1 and vy == 0:
                vx = 0
                vy = 1
            else:
                vx = -1
                vy = 0          
        else:
            if vx == 1 and vy == 0:
                vx = 0
                vy = 1
            elif vx == 0 and vy == 1:
                vx = -1
                vy = 0
            elif vx == -1 and vy == 0:
                vx = 0
                vy = -1
            else:
                vx = 1
                vy = 0   
    
    return vx, vy
        
def create_car(x, y, vx, vy, bs):
    global n
    if(random.random() > P):
        return
    
    vx, vy = decide_turn(x, y, vx, vy)
    
    
    cars.append((x, y, vx, vy, bs, bs, bs, bs))
    
    n = n + 1

def cal_power(d):
    if d == 0:
        temp = -60
    else:
        temp = (-60 - 20*math.log10(d))
        
    return temp

E = 5
T = -110
Pt = -50
Pmin = -125
v_car = 10
P = (2 / 60) * math.exp(-(2 / 60))
road_len = 750
BS = ((750, 750), (2250, 750), (750, 2250), (2250, 2250))
cars = []
n = 0
handoff = 4*[0]
Y = [[], [], [], []]
P_int1 = cal_power(750)
P_int2 = cal_power(750*(2**(1/2)))
total_power = 4*[0]
print(time.asctime(time.localtime(time.time())))

# create_car(road_len, 0, 0, 1, 0, P_int1) # create cars
for i in range(86400):
    leave_cars = []
    
    if i % 10000 == 0:
        print(handoff)
        
    create_car(road_len, 0, 0, 1, 0) # create cars
    create_car(road_len*2, 0, 0, 1, 0)
    create_car(road_len*3, 0, 0, 1, 1)
    create_car(0, road_len, 1, 0, 0)
    create_car(0, road_len*2, 1, 0, 0)
    create_car(0, road_len*3, 1, 0, 2)
    create_car(road_len, road_len*4, 0, -1, 2)
    create_car(road_len*2, road_len*4, 0, -1, 2)
    create_car(road_len*3, road_len*4, 0, -1, 3)
    create_car(road_len*4, road_len, -1, 0, 1)
    create_car(road_len*4, road_len*2, -1, 0, 1)
    create_car(road_len*4, road_len*3, -1, 0, 3)
    
    for id in range(len(cars)): # moving car
        attr = cars[id] 
        x = attr[0] + v_car*attr[2]
        y = attr[1] + v_car*attr[3]
        vx = attr[2]
        vy = attr[3]
        policy1 = attr[4]
        policy2 = attr[5]
        policy3 = attr[6]
        policy4 = attr[7]
        
        # car leaving
        if x > 3000 or x < 0 or y > 3000 or y < 0: 
            leave_cars.append(id)
            continue
            
        # car turning
        if x%750 == 0 and y%750 == 0: 
            vx, vy = decide_turn(x, y, vx, vy)
            
        P_new = -1000
        P_old = 4*[-1000]
        BS_max = -1
        for j in range(4):
            d = ((x-BS[j][0])**2 + (y-BS[j][1])**2)**(1/2)
            P_temp = cal_power(d)
            if j == policy1:
                P_old[0] = P_temp   
            if j == policy2:
                P_old[1] = P_temp   
            if j == policy3:
                P_old[2] = P_temp   
            if j == policy4:
                P_old[3] = P_temp   

            if P_temp > P_new:
                P_new = P_temp
                BS_max = j

        # policy 1
        if BS_max != policy1 and P_new > P_old[0]:
            handoff[0] = handoff[0] + 1
            policy1 = BS_max
            total_power[0] += P_new
        else:
            total_power[0] += P_old[0]

        # policy 2
        if BS_max != policy2 and P_new > P_old[1] and P_old[1] < T:
            handoff[1] = handoff[1] + 1
            policy2 = BS_max
            total_power[1] += P_new
        else:
            total_power[1] += P_old[1]
           
        # policy 3
        if BS_max != policy3 and P_new > P_old[2] + E:
            handoff[2] = handoff[2] + 1
            policy3 = BS_max
            total_power[2] += P_new
        else:
            total_power[2] += P_old[2]
                
        # policy 4
        if BS_max != policy4 and P_new > P_old[3] and P_old[3] < Pmin:
            handoff[3] = handoff[3] + 1
            policy4 = BS_max
            total_power[3] += P_new
        else:
            total_power[3] += P_old[3]
    
        cars[id] = (x, y, vx, vy, policy1, policy2, policy3, policy4)
    
    leave_cars.sort(reverse=True)
    for id in leave_cars: # leaving car
        del cars[id]
        
    for k in range(4):
        Y[k].append(handoff[k])
        

print(time.asctime(time.localtime(time.time())))

# print result
print('Handoffs:')
for i in range(4):
    print('Policy{}: {}'.format(i+1, handoff[i]))

print()
print('Average Power:')
for i in range(4):
    print('Policy{}: {}'.format(i+1, total_power[i]/86400/n))




    
    
X = list(range(86400))

plt.figure(1, figsize=(50, 50))
plt.plot(X, Y[0], 'b-.', label='Best Policy')
plt.plot(X, Y[1], 'r--', label='Threshold Policy')
plt.plot(X, Y[2], 'c', label='Entropy Policy')
plt.plot(X, Y[3], 'm', label='My Policy')
plt.xlabel('time(s)')
plt.ylabel('Handoff')
plt.legend()
plt.show()       
    
    