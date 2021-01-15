def simple_abs(number):
    return -number if number < 0 else number


# Newton's method
def my_sqrt(y, tolerance=0.00005):
    prev = -1.0
    x = 1.0
    while simple_abs(x - prev) > tolerance:
        prev = x
        x = x - (x * x - y) / (2 * x)
    return x


# def abs(a):
#   a = -a if a < 0 else a
#   return a

#
#
# def ft_sqrt(w, g=1, tolerance=0.00001):
#   newGuess = g - (g ** 2 - w) / (2 * (g ** (2 - 1)))
#   if (abs(newGuess - g) < abs(g * tolerance)):
#     return newGuess
#   else:
#     return ft_sqrt(w, newGuess)
#


if __name__ == '__main__':
    # print(ft_sqrt(-10))
	# print(pow(-4, 0.5))
	print(my_sqrt(10.0))
