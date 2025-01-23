import numpy as np

def contraction(polynomial, point):

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
    
    print(p_z,dp_z,ddp_z)

    if abs(dp_z) < 10e-16:     #Wykluczam pochodne bliskie 0 
        return False

    norm_D_N = abs(p_z * ddp_z) / (abs(dp_z)**2)    #||D(N(x))|| = |p(z) * p''(z) / (p'(z))^2|
    
    print(norm_D_N)

    if norm_D_N >= 1:       # Warunek ||D(N(x))|| < 1   (L<1)
        return False

    N_y = point - p_z / dp_z    #Krok metody Newtona N(y) = y - p(y)/p'(y)
    radius = abs(N_y - point) / (1 - norm_D_N)      # Obliczanie promienia R = ||N(y) - y|| / (1 - L)


    epsilon = abs(N_y - point)  #epsilon= ||N(x) - x0||
    print(radius,epsilon)
    if radius >= 2 * epsilon:   #Warunek na R
        return True
    else:
        return False


polynomial = [1.1, 2.1, 0]  # Wielomian x^2 - 3x + 2
point = -1.90909090909+ 0j  # Podejrzewany pierwiastek

if contraction(polynomial, point):
    print(f"Punkt {point} jest miejscem zerowym wielomianu.")
else:
    print(f"Punkt {point} NIE jest miejscem zerowym wielomianu.")
