import math
import time
import random
import pickle

t = 0
duration = 60 * 60 * 5
rate = 0.23
arrive_time = []

while t < duration:
    t = t + random.expovariate(rate)
    arrive_time.append(t)

f = open('arrive_time.pkl','wb')
pickle.dump(arrive_time, f)
f.close()
