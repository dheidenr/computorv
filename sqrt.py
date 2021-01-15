def simple_abs(number):
    return -number if number < 0 else number


def my_sqrt(number, accuracy=0.00005):
    previous_value = -1.0
    root = 1.0
    while accuracy < simple_abs(root - previous_value):
        previous_value = root
        root = root - (root * root - number) / (2 * root)
    return root
