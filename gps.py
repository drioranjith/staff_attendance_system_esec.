# gps.py
import math

# Set your allowed location
ALLOWED_LAT = 11.3418     # Erode Sengunthar Engineering College
ALLOWED_LON = 77.7177
ALLOWED_RADIUS = 1000      # 1 km

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def is_inside_allowed_area(lat, lon):
    dist = calculate_distance(lat, lon, ALLOWED_LAT, ALLOWED_LON)
    return (dist <= ALLOWED_RADIUS, dist)
# Example usage:
if __name__ == "__main__":
    test_lat = 11.3420
    test_lon = 77.7180
    valid, distance = is_inside_allowed_area(test_lat, test_lon)
    if valid:
        print(f"Inside allowed area. Distance: {distance} meters")
    else:
        print(f"Outside allowed area. Distance: {distance} meters")
