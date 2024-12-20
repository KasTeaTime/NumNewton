#Program przyjmuje dane z pliku przekazywanego do programu w pierwszej linijce znajduje się stopień wielomianu zaś w kolejnych współczynniki. 
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
                    coefficients.append(line)  # Zamiana tekstu na liczbę lub liczbę zespoloną
    return(degree, coefficients)

def contraction(polynomial, derivative, root):
    L = 0  # Stała (musi być mniejsza od 1)
    r = 1e-3  # Małe otoczenie wokół pierwiastka
    
    for x in np.linspace(root.real - r, root.real + r, 10):
        for y in np.linspace(root.imag - r, root.imag + r, 10):
            z1 = complex(x, y)  #punkt testowy
            z2 = root           #punkt stały
            try:
                N_z1 = z1 - polynomial(z1) / derivative(z1)
                N_z2 = z2 - polynomial(z2) / derivative(z2)
                L = max(L, abs(N_z1 - N_z2) / abs(z1 - z2))
            except ZeroDivisionError:
                continue

    return L < 1
     


def newton(coeffs, guess_num = 100, max_iter=100000, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()
    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    guesses = [complex(np.random.uniform(-50, 50), np.random.uniform(-10, 10)) for _ in range(guess_num)]   #szukamy na przedziale -50 50
    
    for guess in guesses:
        x = guess
        for _ in range(max_iter):
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
            x = x_next
        
        if complex(-0) in roots:
            print("a")

        # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
        if not any(abs(x - r) < tolerance for r in roots):
                roots.append(x)

    
    return roots                     

    
#wczytanie danych   
if len(sys.argv) < 2:
    print("Podaj nazwe pliku")
    exit()
data = sys.argv[1]

#print(open(data))
degree, coefficients = reading(data)
print(degree)
print(coefficients)
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]


roots = newton(coefficients)

print("miejsca zerowe wielomianu")
print(np.round(roots,2))
if degree - len(roots) != 0:
    print( "podejrzenie", (degree - len(roots)), " pierwiastkow wielokrotnych")
