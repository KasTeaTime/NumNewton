#Program przyjmuje dane z pliku przekazywanego do programu. 
#W pierwszej linijce znajduje się stopień wielomianu i ewentualny komentarz zaś w kolejnych współczynniki. 
#Dane powinny być odzielone enterami
#Jednostka urojona powinna być zapisana jako i lub j. 
#Szukamy miejsca zerowego na przedziale -50 50

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
    r =0.1 #Promień poszukiwać 
    root = N_root+ polynomial(N_root) / derivative(N_root) #Krok obliczający kolejne przybliżenie miejsca zerowego

    L=-(abs(N_root - root)/r-1) #Stała 

 
    if abs(root - N_root) < 10e-6: # Czy punkt początkowy jest daleko od rzeczywistego miejsca zerowego
        # Sprawdzenie kontrakcji w kuli o promieniu r
        for theta in np.linspace(0, 2 * np.pi, 100):  # Generowanie kątów kuli dla których sprawdzamy kontrakcję
            for rad in np.linspace(0, r, 100):       # Generowanie promieni kuli dla których sprawdzamy kontrakcję
                z = root + rad * (np.cos(theta) + 1j * np.sin(theta)) 

                N_z = z - polynomial(z) / derivative(z)     #kula
                try:
                    # Sprawdzenie warunku |N(z) - z0| <= L |z - z0| + |N(z0) - z0|
                    if abs(N_z - root) < L * abs(z - root) + abs(N_root - root):
                        return False
                    else:
                        return True
                except ZeroDivisionError:
                    continue
    else:
        return False
     

def newton(coeffs, guess_num = 1000, max_iter=100, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()
    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    guesses = [complex(np.random.uniform(-50, 50), np.random.uniform(-50, 50)) for _ in range(guess_num)]   #Szukamy na przedziale -50 50

    for iter_guess, guess in enumerate(guesses):
        if len(roots) < degree:    
            x = guess

            for i in range(max_iter):
                f_x = polynomial(x)
                f_prime_x = derivative(x)

                if abs(f_prime_x) < 1e-15: #Czy moduł z liczby nie jest zbyt blisko 0 
                    print("Uwaga: Pochodna dla wartości podejrzewanej o bycie miejscem zerowym jest bliska zeru, kontynuuję obliczenia")

                x = x - f_x / f_prime_x

            if contraction(polynomial, derivative, x):
                if not any(abs(x - r) < tolerance for r in roots): # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
                    roots.append(x)
    return roots                     

    
#wczytanie danych   
if len(sys.argv) < 2:
    print("Podaj nazwe pliku")
    exit()
data = sys.argv[1]


degree, coefficients = reading(data)
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]

roots = newton(coefficients)
np.set_printoptions(precision=2, floatmode='fixed', linewidth=100, suppress=True) #Formatowanie wypisywania w konsoli
print("miejsca zerowe wielomianu")
print(np.round(roots,2)) 
if degree - len(roots) != 0:
    print( "podejrzenie", (degree - len(roots)), " pierwiastkow wielokrotnych")
