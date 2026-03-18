import math


r = 0.0665 #m
l = 0.1135 #l
front_theta =  math.radians(0+90)
left_theta =  math.radians(120+90) 
right_theta =  math.radians(240+90)



def cal_wheel_speed(Vx, Vy, W):
    u1 = -math.sin(front_theta)*Vx + math.cos(front_theta)*Vy + l*W
    u2 = -math.sin(left_theta)*Vx + math.cos(left_theta)*Vy + l*W
    u3 = -math.sin(right_theta)*Vx + math.cos(right_theta)*Vy + l*W
    w1 = u1/r
    w2 = u2/r
    w3 = u3/r
    
    return w1, w2, w3 

print(cal_wheel_speed(0,1,0))
print(cal_wheel_speed(1,0,0))