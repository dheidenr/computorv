def simple_abs(number):
    return -number if number < 0 else number


def my_sqrt(y, tolerance=0.00005):
    prev = -1.0
    x = 1.0
    while simple_abs(x - prev) > tolerance:
        prev = x
        x = x - (x * x - y) / (2 * x)
    return x
