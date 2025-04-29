


def get_closest_driver(drivers, pickup_address):
    """
    Get the driver closest to the pickup address.
    """
    closest_driver = None
    closest_distance = float('inf')

    for driver in drivers:
        distance = driver.calculate_distance(pickup_address.latitude, pickup_address.longitude)
        if distance < closest_distance:
            closest_distance = distance
            closest_driver = driver

    return closest_driver, closest_distance

def get_arrival_time(distance_km: float, average_speed_kmh: float = 60.0) -> int:
    """
    Calcula el tiempo estimado de llegada en minutos, redondeado al entero más cercano.
    
    :param distance_km: Distancia en kilómetros.
    :param average_speed_kmh: Velocidad promedio en km/h. Por defecto 60 km/h.
    :return: Tiempo estimado de llegada en minutos (int).
    """
    if average_speed_kmh <= 0:
        raise ValueError("La velocidad promedio debe ser mayor que cero.")
    
    estimated_minutes = (distance_km / average_speed_kmh) * 60
    return round(estimated_minutes)