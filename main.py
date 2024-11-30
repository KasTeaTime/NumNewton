import numpy as np
from numpy.polynomial import Polynomial

def reading(filename):
    with open(filename) as file:
        for index, line in enumerate(file):
            if index == 0:
                degree=int(line[:-1])
            elif index==1:
                    coefficients = line.split(",")
                    print(coefficients)
    return(degree, coefficients)
    
                    


                    

ep=0.001
x0=5
           
degree, coefficients = reading("data.txt")


coefficients = complex(coefficients)
print(coefficients)