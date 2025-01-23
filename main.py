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

def contraction(polynomial, point):
    # if point==0j:
    #     point= 0+0j

    #Obliczenie wartości wielomianu i jego pochodnych w punkcie
    def p(z):
        sum=0
        for i, a in enumerate(reversed(polynomial)):    #a to współczynniki wielomianu
            sum = sum + a * z**i
        return sum

    def dp(z):
        sum=0
        for i, a in enumerate(reversed(polynomial)):
            if i > 0:
                sum = sum +i * a * z**(i-1)
        return sum

    def ddp(z):
        sum=0
        for i, a in enumerate(reversed(polynomial)):
            if i > 1:
                sum=sum + i * (i-1) * a * z**(i-2) 
        return sum
    
    #Obliczenia wartości wielomianu i jego pochodnych w punkcie podejrzanym o bycie miejscem zerowym
    p_z = p(point)
    dp_z = dp(point)
    ddp_z = ddp(point)
    
    if abs(dp_z) < 10e-6:     #Wykluczam pochodne bliskie 0 
        return False

    norm_D_N = abs(p_z * ddp_z) / (abs(dp_z)**2)    #||D(N(x))|| = |p(z) * p''(z) / (p'(z))^2|
    
    if norm_D_N >= 1:       # Warunek ||D(N(x))|| < 1   (L<1)
        return False

    N_y = point - p_z / dp_z    #Krok metody Newtona N(y) = y - p(y)/p'(y)
    radius = abs(N_y - point) / (1 - norm_D_N)      # Obliczanie promienia R = ||N(y) - y|| / (1 - L)

#########################SPR CZY DZIAŁA
    if p(point) < 1e-6:
        print("to jest pierwiastek",point, "miau")
    else:
        print("to nie jest pierwiastek",point)            
##########################################
    
    epsilon = abs(N_y - point)  #epsilon= ||N(x) - x0||
    if radius >= 2 * epsilon:   #Warunek na R
        return True
    else:
        return False
     

def newton(coeffs, guess_num = 10, max_iter=100, tolerance=10e-6): 
    degree = len(coeffs) - 1
    roots = []
    polynomial = Polynomial(coeffs)
    derivative = polynomial.deriv()
    print(polynomial)
    
    # Losowy wybór początkowych punktów startowych w płaszczyźnie zespolonej
    guesses = [complex(np.random.uniform(-50, 50), np.random.uniform(-50, 50)) for _ in range(guess_num)]   #Szukamy na przedziale -50 50

    for iter_guess, guess in enumerate(guesses):
        if len(roots) < degree:    
            x = guess

            for i in range(max_iter):
                f_x = polynomial(x)
                f_prime_x = derivative(x)

                if abs(f_prime_x) < 1e-18: #Czy moduł z liczby nie jest zbyt blisko 0 
                    print("Uwaga: Pochodna dla wartości podejrzewanej o bycie miejscem zerowym jest bliska zeru, kontynuuję obliczenia")


                x = x - f_x / f_prime_x


            if contraction(coeffs, x):
                if not any(abs(x - r) < tolerance for r in roots): # Dodaj pierwiastek do listy, jeśli nie jest zbyt blisko istniejących
                    roots.append(x)
    return roots                     

    
# wczytanie danych   

if len(sys.argv) < 2:
    print("Podaj nazwe pliku")
    exit()
data = sys.argv[1]

# data="data2.txt"

degree, coefficients = reading(data)
coefficients = [c.replace('i', 'j') for c in coefficients] 
coefficients = [complex(c) for c in coefficients]

roots = newton(coefficients)
np.set_printoptions(precision=2, floatmode='fixed', linewidth=100, suppress=True) #Formatowanie wypisywania w konsoli
print("miejsca zerowe wielomianu")
print(np.round(roots,2)) 
if degree - len(roots) != 0:
    print( "podejrzenie", (degree - len(roots)), " pierwiastkow wielokrotnych")
