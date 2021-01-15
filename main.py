from argparse import ArgumentParser

from sqrt import my_sqrt

DOT = "."
NUMBERS = "0123456789"
SIGNS = "+-"
MULTI = '*'
POWER = '^'
VARIABLE = 'xX'


def convert_sign_list(signs:list):
    new_signs = []
    for letter in signs:
        if letter in SIGNS:
            new_signs.append('-' if letter == '+' else '+')
        else:
            error_input()
    return new_signs


def error_input():
    print('Ошибка ввода')
    exit()


def single_coeff(line: str, sign: str, coefs: list, variables: list, degrees: list):
    length = 0
    if line.isdigit():
        cursor, number = parse_number(line, sign)
        coefs.append(number)
        variables.append('X')
        degrees.append(0)
        length += cursor

    return length, coefs, variables, degrees


def parse_coef_variable_degree(line: str, sign: str, coefs: list, variables: list, degrees: list):
    if line[0] not in NUMBERS and  line[0] not in VARIABLE:
        error_input()

    if line.isdigit():
        single_coeff(line, sign, coefs, variables, degrees)
        return coefs, variables, degrees

    cursor = 0
    if line[cursor] not in VARIABLE:
        length, number = parse_number(line[cursor:], sign)
        cursor += length
        coefs.append(number)
    else:
        variables.append(line[cursor])
        coefs.append(1)
        cursor += 1
        if cursor >= len(line):
            degrees.append(1)
            return coefs, variables, degrees

        if line[cursor] not in POWER:
            if line[cursor] in SIGNS:
                degrees.append(1)
            else:
                error_input()
        else:
            cursor += 1

        if line[cursor] not in NUMBERS:
            error_input()
        length, number = parse_number(line[cursor:], '+')
        cursor += length
        degrees.append(number)
        return coefs, variables, degrees

    if line[cursor] not in MULTI:
        error_input()
    else:
        cursor += 1

    if line[cursor] in VARIABLE:
        variables.append(line[cursor])
        cursor += 1
    else:
        error_input()
    if cursor >= len(line):
        degrees.append(1)
        return coefs, variables, degrees

    if line[cursor] not in POWER:
        if line[cursor] in SIGNS:
            degrees.append(1)
        else:
            error_input()
    else:
        cursor += 1

    if line[cursor] not in NUMBERS:
        error_input()
    length, number = parse_number(line[cursor:], '+')
    cursor += length
    degrees.append(number)
    return coefs, variables, degrees


def parse_number(line: str, sign: str):
    number_line = ''
    for letter in line:
        if letter in NUMBERS or letter in DOT:
            number_line += letter
        else:
            break
    if DOT in number_line:
        number = float(sign + number_line)
    else:
        number = int(sign + number_line)
    return len(number_line), number


def get_signs(line: str):
    signs_list = []
    if line[0] in NUMBERS or line[0] in VARIABLE:
        signs_list.append('+')
    for letter in line:
        if letter in SIGNS:
            signs_list.append(letter)
    return signs_list


def parser(line: str):
    line = ''.join((line).split())

    if '=' not in line:
        print('Некорректное выражение, нет =')
        exit()
    polynomial = line.split('=')
    signs_list = []
    signs_list.append(get_signs(polynomial[0]))
    signs_list.append(get_signs(polynomial[1]))
    if len(polynomial) == 2:
        polynomial[0] = polynomial[0].replace('+', ' ').replace('-', ' ').split(' ')
        polynomial[1] = polynomial[1].replace('+', ' ').replace('-', ' ').split(' ')
    else:
        print('Некорректный ввод, слишком много =')
        exit()
    if polynomial[0][0] == '':
        del polynomial[0][0]
    coefs = []
    variables = []
    degrees = []

    signs_list[1] = convert_sign_list(signs_list[1])
    for word, sign in zip(polynomial[0], signs_list[0]):
        parse_coef_variable_degree(word, sign, coefs, variables, degrees)
    for word, sign in zip(polynomial[1], signs_list[1]):
        parse_coef_variable_degree(word, sign, coefs, variables, degrees)
    return coefs, variables, degrees


def get_reduced(coefs: list, variables: list, degrees: list):
    degree_coef = {}
    for co, var, deg in zip(coefs, variables, degrees):
        if deg in degree_coef:
            degree_coef[deg][0] += co
        else:
            degree_coef[deg] = [co, var]
    return degree_coef


def print_reduced(degree_coef:dict):
    line = ''
    max_degree =  max(degree_coef.keys())
    if degree_coef is not None:
        for iter in range(max_degree + 1):
            if iter in degree_coef:
                if degree_coef[iter][0] != 0 or (max_degree == 0 and degree_coef[iter][0] == 0):
                    if iter == 0:
                        line += str(degree_coef[iter][0]) + ' '
                    if iter == 1:
                        if degree_coef[iter][0] < 0:
                            if line == '':
                                sign = '-'
                            else:
                                sign = '- '
                            number = str(-degree_coef[iter][0])
                        else:
                            if line == '':
                                sign = ''
                            else:
                                sign = '+ '
                            number = str(degree_coef[iter][0])
                        line += sign + number + ' * ' + str(degree_coef[iter][1]) + ' '
                    if iter > 1:
                        if degree_coef[iter][0] < 0:
                            if line == '':
                                sign = '-'
                            else:
                                sign = '- '
                            number = str(-degree_coef[iter][0])
                        else:
                            if line == '':
                                sign = ''
                            else:
                                sign = '+ '
                            number = str(degree_coef[iter][0])
                        line += sign + number + ' * ' + str(degree_coef[iter][1]) + POWER + str(iter) + ' '
        line = line.strip() + ' = 0'
        if len(line) >= 2:
            if (line[0] in SIGNS) and line[1] == ' ':
                line = line[0] + line[2:]
        print(f'Reduced form: {line}')


def max_degree_solver_one(degree_coef:dict):
    max_degree = max(degree_coef.keys())
    if max_degree == 1:
        if degree_coef[1][0] == 0:
            if degree_coef[0][0] == 0:
                print("The polynomial has an infinite number of solutions")
                exit()
            else:
                print("Polynomial has no solutions")
                exit()
        if degree_coef[1][0] == 0:
            print("The polynomial has an infinite number of solutions")
            exit()
        print(f"The solution is: {-degree_coef[0][0] / degree_coef[1][0]}")


def solver(degree_coef:dict):
    # zero
    max_degree = max(degree_coef.keys())
    if max_degree == 0:
        if degree_coef[0][0] == 0:
            print("The polynomial has an infinite number of solutions")
            exit()
        else:
            print("Polynomial has no solutions")
            exit()
    # one
    max_degree_solver_one(degree_coef)
    # two
    if max_degree == 2:
        if degree_coef[0][0] == 0:
            max_degree_solver_one(degree_coef)
        D = float(degree_coef[1][0] ** 2 - 4 * degree_coef[2][0] * degree_coef[0][0])
        if D > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            solution_one = (-degree_coef[1][0] + my_sqrt(D)) / (2 * degree_coef[2][0])
            solution_two = (-degree_coef[1][0] - my_sqrt(D)) / (2 * degree_coef[2][0])
            print(f"%.5f" % solution_one)
            print(f"%.5f" % solution_two)
        if D == 0:
            print("The discrimination is zero so there is only one solution::")
            # if degree_coef[1][0] == 0:
            #     single_solution = 0
            # else:
            single_solution = (-1 * (degree_coef[1][0] / (2 * degree_coef[2][0])))
            single_solution = single_solution if single_solution != 0 else 0
            print("%.5f" % single_solution)
        if D < 0:
            print("Discriminant is strictly negative, the two solutions are:")
            real = ((-degree_coef[1][0]) / (2 * degree_coef[2][0]))
            imag = (my_sqrt(-D) / (2 * degree_coef[2][0]))
            print("First solution:", "real: %.5f +" % real, "image:%.5f" % imag)
            print("Second solution:", "real: %.5f -" % real, "image:%.5f" % imag)


def full_coenf_zerro(degree_coef):
    max_degree = max(degree_coef.keys())
    for i in range(max_degree):
        if i not in degree_coef:
            degree_coef[i] = [0, 'X']
    return degree_coef


def degree_exit(degrees):
    print(f'Polynomial degree: {max(degrees)}')
    if max(degrees) > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        exit()


def solution(polynomial: str):
    coefs, variables, degrees = parser(polynomial)
    if len(coefs) != len(variables) or len(variables) != len(degrees):
        error_input()
    degree_coef = get_reduced(coefs, variables, degrees)
    degree_coef = full_coenf_zerro(degree_coef)
    print_reduced(degree_coef)
    degree_exit(degrees)
    solver(degree_coef)


def get_string():
    parser = ArgumentParser()
    parser.add_argument("polynomial", type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_string()
    polynomial = args.polynomial.strip()
    solution(polynomial)
