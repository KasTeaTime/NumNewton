import numpy as np

def is_zero_by_contraction(polynomial, point, epsilon=1e-6):
    """
    Sprawdza, czy dany punkt jest miejscem zerowym wielomianu za pomocą kontrakcji.
    
    Args:
        polynomial (list): Współczynniki wielomianu [a_n, a_{n-1}, ..., a_0].
        point (complex): Punkt podejrzewany o bycie miejscem zerowym.
        epsilon (float): Tolerancja dla warunków kontrakcji.
    
    Returns:
        bool: True, jeśli punkt spełnia warunki kontrakcji, False w przeciwnym razie.
    """
    # Funkcje pomocnicze do obliczania wartości wielomianu i jego pochodnych
    def p(z):
        """Oblicza wartość wielomianu w punkcie z."""
        return sum(a * z**i for i, a in enumerate(reversed(polynomial)))

    def dp(z):
        """Oblicza wartość pierwszej pochodnej wielomianu w punkcie z."""
        return sum(i * a * z**(i-1) for i, a in enumerate(reversed(polynomial)) if i > 0)

    def ddp(z):
        """Oblicza wartość drugiej pochodnej wielomianu w punkcie z."""
        return sum(i * (i-1) * a * z**(i-2) for i, a in enumerate(reversed(polynomial)) if i > 1)

    # Obliczenia wartości wielomianu i jego pochodnych w punkcie
    p_z = p(point)  # Wartość wielomianu w punkcie
    dp_z = dp(point)  # Wartość pierwszej pochodnej w punkcie
    ddp_z = ddp(point)  # Wartość drugiej pochodnej w punkcie

    # Obliczanie normy ||D(N(x))|| = |p(z) * p''(z) / (p'(z))^2|
    try:
        norm_D_N = abs(p_z * ddp_z) / (abs(dp_z)**2)
    except ZeroDivisionError:
        return False  # Jeśli p'(z) = 0, kontrakcja nie działa

    print(norm_D_N)
    # Warunek kontrakcji: ||D(N(x))|| musi być mniejsze od 1
    if norm_D_N >= 1:
        return False

    # Obliczanie promienia kontrakcji R = ||N(y) - y|| / (1 - ||D(N(x))||)
    # Operator Newtona: N(y) = y - p(y)/p'(y)
    N_y = point - p_z / dp_z  # Nowa iteracja Newtona
    diff = abs(N_y - point)  # Odległość między kolejną iteracją a punktem początkowym
    radius = diff / (1 - norm_D_N)  # Promień kontrakcji

    # Sprawdzenie, czy promień kontrakcji R spełnia warunek
    if radius >= 2 * epsilon:
        return False

    # Jeśli wszystkie warunki są spełnione, uznajemy punkt za miejsce zerowe
    return True


polynomial = [2.1, 1.1, 0]  # Wielomian 2.1z^2 + 1.1z
point = -1.90909 + 0j  # Punkt podejrzewany o bycie miejscem zerowym

result = is_zero_by_contraction(polynomial, point)
print(result)  # Powinno zwrócić True
