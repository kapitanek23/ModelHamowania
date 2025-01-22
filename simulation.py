def simulate_braking(v0=30.0, dt=0.1, c=0.1, m=1000.0, t_max=60.0):
    """
    Symulacja spowolnienia pojazdu przy założeniu oporu proporcjonalnego do v^2.
    v0    - początkowa prędkość [m/s]
    dt    - krok czasowy [s]
    c     - współczynnik oporu
    m     - masa pojazdu [kg]
    t_max - maksymalny czas symulacji [s]
    
    Zwraca krotkę (time_points, velocity_points, position_points):
      - time_points: lista chwil czasu
      - velocity_points: lista prędkości w kolejnych krokach
      - position_points: lista położeń w kolejnych krokach
    """

    time_points = []
    velocity_points = []
    position_points = []

    # Inicjalizacja warunków początkowych
    t = 0.0
    v = v0
    x = 0.0

    while t <= t_max and v > 0:
        time_points.append(t)
        velocity_points.append(v)
        position_points.append(x)

        # Siła oporu ~ c * v^2
        F_drag = c * v**2
        # Przyspieszenie (ujemne) wynikające z tej siły
        a = F_drag / m

        # Aktualizacja prędkości (równanie różnicowe)
        v_new = v - a * dt
        # Aktualizacja położenia
        x_new = x + v * dt

        # Przejście do następnego kroku
        v = max(v_new, 0)   # żeby nie zejść poniżej 0
        x = x_new
        t += dt

    return time_points, velocity_points, position_points
