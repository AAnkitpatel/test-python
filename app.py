import time
import random
import subprocess

def rand():
    ran=random.randint(100,1000)
    print(ran, end=' ')

while True:
    print(rand(), 'this is python app....')
    time.sleep(2)
    