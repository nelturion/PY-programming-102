def addition(x, y):
    return float(x) + float(y)


def substracition(x, y):
    return float(x) - float(y)


def multiply(x, y):
    return float(x) * float(y)


def divide(x, y):
    if float(y) == 0:
        return "Делить на ноль можно, но только осторожно. Я не осторожный."
    else:
        return float(x) / float(y)


if __name__ == '__main__':
    a = int(input("Калькулятор Prostecki\nВведите первое число: "))
    b = int(input("Введите второе число: "))
    operation = input("Введите обозначение математической операции (+,-,*,/): ")

    ops = {'+': addition, '-': substracition, '*': multiply, '/': divide}

    print(ops[operation](a, b))
