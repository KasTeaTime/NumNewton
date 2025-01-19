import numpy as np

def contraction(polynomial, x0):
    radius = 0.05  # Promień większej kuli w obrębie którego sprawdzamy kontrakcję
    resolution = 1000 #Liczba punktów w kuli

    derivative = polynomial.deriv()           # Wyznaczenie pochodnej i drugiej pochodnej wielomianu
    derivative2 = derivative.deriv()

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



# Przykład użycia
poly = np.poly1d([1e-14, 1e-14, 0])  # Wielomian f(x) = x^2 - 0
x0 = 0.01+0j # Podejrzane miejsce zerowe


is_contraction= contraction(poly, x0)
print(f"Czy funkcja iteracyjna jest kontrakcją w kuli? {is_contraction}")
