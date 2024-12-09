#Program przyjmuje dane z pliku przekazywanego do programu. 
# W pierwszej linijce znajduje się stopień wielomianu i ewentualny komentarz zaś w kolejnych współczynniki. 
#Dane powinny być odzielone enterami
#Jednostka urojona powinna być zapisana jako i lub j. 

import numpy as np
import sys
from numpy.polynomial import Polynomial

def reading(filename):
    coefficients=[]
    with open(filename) as file:
        for index, line in enumerate(file):
            line = line.strip() # Usunięcie białych znaków na początku i końcu linii
            if index == 0:
                degree = int(line.split()[0])
            else:
                if line and not line.startswith("#"):   # Pomiń puste linie i komentarze
                    coefficients.append(line)  
    return(degree, coefficients)

def contraction(polynomial, derivative, N_root):
    L =0.1  # Stała (musi być mniejsza od 1)
    #N_root = root - polynomial(root) / derivative(root)
    root = N_root+ polynomial(N_root) / derivative(N_root)
    
    r = abs(N_root - root) / (1 - L)
    print(N_root - root)

    #if abs(r - N_root) < 10e-6:
    #    return False

    # Sprawdzenie kontrakcji w kuli o promieniu r
    for theta in np.linspace(0, 2 * np.pi, 100):  # Kąt
        for rad in np.linspace(0, r, 100):       # Promień
            z = root + rad * (np.cos(theta) + 1j * np.sin(theta))

            N_z = z - polynomial(z) / derivative(z)
            try:
                # Sprawdzenie warunku |N(z) - z0| <= L |z - z0| + |N(z0) - z0|
                if abs(N_z - root) < L * abs(z - root) + abs(N_root - root):
                    return False
            except ZeroDivisionError:
                continue
    return True
     

def newton(coeffs, guess_num = 100, max_iter=100, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()
    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    guesses = [complex(np.random.uniform(-50, 50), np.random.uniform(-50, 50)) for _ in range(guess_num)]   #szukamy na przedziale -50 50

    for guess in guesses:
        #if len(roots) < degree:
        if True:    
            x = guess
            for i in range(max_iter):
                f_x = polynomial(x)
                f_prime_x = derivative(x)

                if abs(f_prime_x) < 1e-14: #czy moduł z liczby nie jest zbyt blisko 0 
                    print("Terrible precision ")
                
                x_next = x - f_x / f_prime_x
                
                # Sprawdzenie zbieżności

                if abs(x_next - x) < tolerance:
                    if contraction(polynomial, derivative, x_next):
                        x = x_next
                        break
            # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
            if not any(abs(x - r) < tolerance for r in roots): 
                roots.append(x) 
    return roots                     

    
#wczytanie danych   
# if len(sys.argv) < 2:
#     print("Podaj nazwe pliku")
#     exit()
# data = sys.argv[1]

data = 'data.txt'

def P(x):
    return x**2 - 2

def P_prime(x):
    return 2 * x

root = 1.4  # Blisko sqrt(2)
print(contraction(P, P_prime, root))  # Oczekiwany wynik: True
root = 10  # Daleko od sqrt(2)
print(contraction(P, P_prime, root))  # Oczekiwany wynik: False









degree, coefficients = reading(data)
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]

#roots = newton(coefficients)
# np.set_printoptions(precision=2, floatmode='fixed', linewidth=100, suppress=True) #Formatowanie wypisywania w konsoli
# print("miejsca zerowe wielomianu")
# print(np.round(roots,2)) 
# if degree - len(roots) != 0:
#     print( "podejrzenie", (degree - len(roots)), " pierwiastkow wielokrotnych")
