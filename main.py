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

def contraction(polynomial, x0):
    radius = 0.5  # Promień większej kuli w obrębie którego sprawdzamy kontrakcję
    resolution = 1000 #Liczba punktów w kuli

    derivative = polynomial.deriv()           # Wyznaczenie pochodnej i drugiej pochodnej wielomianu
    derivative2 = derivative.deriv()

    print(derivative,"klu", derivative2)

    def N(x):       #Krok metody Newtona
        return x - polynomial(x) / derivative(x)

    def derivative_N(x):    #Wyznaczenie pochodnej N(x)
        return 1 - (derivative(x)**2 - polynomial(x) * derivative2(x)) / (derivative(x)**2)      

    x_values = np.linspace(x0 - radius, x0 + radius, resolution)        #Dyskretyzacja większej kuli
    epsilon = 0     #Wartości startowe
    L = 0

    for x in x_values:  #Dla każdego punktu na kuli bierzemy maksymalną wartość L i epsilon
        if(abs(derivative_N(x)) > L ):  # L=||dN(x)/dx||
            L = abs(derivative_N(x))

        if(abs(N(x) - x0)> epsilon ):   #epsilon= ||N(x) - x0||
            epsilon = abs(N(x) - x0)    #maksymalna odległość N(x) od podejrzanego miejsca zerowego x0  w całej kuli

    if L >= 1:          #Warunek L < 1
        return False

    for x in x_values:    #Sprawdzanie warunku kontrakcji: |N(x) - x0| <= L |x - x0| + epsilon ; na podstawie wzoru 51 i 34 (R = epsilon/(1-L)) z wykładu
        if abs(N(x) - x0) > L * abs(x - x0) + epsilon:
            return False    

    return True
     

def newton(coeffs, guess_num = 100, max_iter=100, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()

    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    # guesses = [complex(np.random.uniform(-10, 10), np.random.uniform(-10, 10)) for _ in range(guess_num)]   #Szukamy na przedziale -50 50
    guesses=[complex(1,0)]

    for iter_guess, guess in enumerate(guesses):
        if len(roots) < degree:    
            x = guess

            for i in range(max_iter):
                f_x = polynomial(x)
                f_prime_x = derivative(x)

                if abs(f_prime_x) < 1e-18: #Czy moduł z liczby nie jest zbyt blisko 0 
                    print("Uwaga: Pochodna dla wartości podejrzewanej o bycie miejscem zerowym jest bliska zeru, kontynuuję obliczenia")


                x = x - f_x / f_prime_x


            if contraction(polynomial, x):
                if not any(abs(x - r) < tolerance for r in roots): # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
                    roots.append(x)
    return roots                     

    
#wczytanie danych   
# if len(sys.argv) < 2:
#     print("Podaj nazwe pliku")
#     exit()
# data = sys.argv[1]

data="data3.txt"

degree, coefficients = reading(data)
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]

roots = newton(coefficients)
np.set_printoptions(precision=2, floatmode='fixed', linewidth=100, suppress=True) #Formatowanie wypisywania w konsoli
print("miejsca zerowe wielomianu")
print(np.round(roots,2)) 
if degree - len(roots) != 0:
    print( "podejrzenie", (degree - len(roots)), " pierwiastkow wielokrotnych")
