""" Основной код лабы №1 """


def addition(first_arg, second_arg):
    """Функция сложения"""
    return float(first_arg) + float(second_arg)


def substracition(first_arg, second_arg):
    """Функция вычитания"""
    return float(first_arg) - float(second_arg)


def multiply(first_arg, second_arg):
    """Функция умножения"""
    return float(first_arg) * float(second_arg)


def divide(first_arg, second_arg):
    """Функция деления"""
    return "Делить на ноль нельзя" if float(second_arg) == 0 else float(first_arg) / float(second_arg)


if __name__ == "__main__":
    a = int(input("Калькулятор Prostecki\nВведите первое число: "))
    b = int(input("Введите второе число: "))
    operation = input("Введите обозначение математической операции (+,-,*,/): ")

    ops = {"+": addition, "-": substracition, "*": multiply, "/": divide}

    print(ops[operation](a, b))
