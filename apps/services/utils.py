


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

def get_arrival_time(distance_km):
    """
    Calculate the estimated arrival time based on distance.
    Assuming an average speed of 60 km/h.
    """
    average_speed_kmh = 60
    estimated_arrival_minutes = (distance_km / average_speed_kmh) * 60
    return estimated_arrival_minutes