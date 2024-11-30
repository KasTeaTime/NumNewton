import numpy as np
from numpy.polynomial import Polynomial

def reading(filename):
    with open(filename) as file:
        for index, line in enumerate(file):
            if index == 0:
                degree=int(line[:-1])
            elif index==1:
                    coefficients = line.split(",")
    return(degree, coefficients)

def gauss_zero(coeffs, guess_num = 10, max_iter=1000, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()
    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    guesses = [complex(np.random.uniform(-10, 10), np.random.uniform(-10, 10)) for _ in range(guess_num)]
    
    for guess in guesses:
        x = guess
        for _ in range(max_iter):
            f_x = polynomial(x)
            f_prime_x = derivative(x)
            
            print("kluseczka")
            if abs(f_prime_x) < 1e-14: 
                print(f_prime_x)
                print("klu")
                print(abs(f_prime_x))
                print("Terrible precision :(")
            
            x_next = x - f_x / f_prime_x
            
            # Sprawdzenie zbieżności
            if abs(x_next - x) < tolerance:
                x = x_next
                break
            
            x = x_next
        
        # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
        if not any(abs(x - r) < tolerance for r in roots):
            #if zbiega to 
                roots.append(x)

    
    return roots
##################################                      


                    
#wczytanie danych       
degree, coefficients = reading("data.txt")
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]
print(coefficients)



roots = gauss_zero(coefficients)
print(roots)