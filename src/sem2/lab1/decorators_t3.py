import sys
import time
from functools import wraps


def logger(show_magic_methods=True):
    """
        Задание 3 - декоратор класса без параметра:
        Реализовать декоратор logger для класса, который выводит имя класса, имя метода (включая все магические методы),
        аргументы и время выполнения. После добавить флаг show_magic_methods, который влияет на то, будут логироваться
        магические методы или нет. Можно добавить вывод результата.

        >>> @logger(show_magic_methods=False)
        ... class SimpleCalc:
        ...     def __init__(self, val):
        ...         self.val = val
        ...     def add(self, x):
        ...         return self.val + x

        >>> calc_obj = SimpleCalc(10)   # тут можно сделать сложно и (возможно) правильно, но так как доктест использует отдельную среду
        >>>                             # выполнения не зависящую от глобальных переменных, в которых ищется имя нашей,
        >>>                             # то в тестах тут будет unknown
        >>> calc_obj.add(5) # doctest: +ELLIPSIS
        [LOG] OBJECT: unknown object
          CLASS: SimpleCalc | METHOD: add
          ARGUMENTS: args=(5,), kwargs={}
          EXEC TIME: ... sec
          RESULT:    15
        15
    """

    def class_decorator(cls):
        for attr_name, attr_value in list(cls.__dict__.items()):
            if callable(attr_value):
                is_magic_method = attr_name.startswith("__") and attr_name.endswith("__")

                if is_magic_method and not show_magic_methods:
                    continue

                def make_wrapper(method_name, original_method):
                    @wraps(original_method)
                    def method_wrapper(self, *args, **kwargs):
                        cmd_silent = "--silent" in sys.argv
                        global_silent = globals().get('silent', False)
                        should_be_silent = cmd_silent or global_silent

                        start_time = time.perf_counter()
                        try:
                            result = original_method(self, *args, **kwargs)
                            return result
                        finally:
                            duration = time.perf_counter() - start_time
                            if not should_be_silent:
                                obj_name = "unknown object"  # уязвимый способ узнать имя объекта (неуязвимый не придумал)
                                for name, value in globals().items():
                                    if value is self:       # уязвим он потому что мы ищем название переменной по ее значению, а значения могут совпадать
                                        obj_name = name     # к тому же на одно и то же значение в памяти может ссылаться много переменных с разными именами
                                        break
                                print(f"[LOG] OBJECT: {obj_name}")
                                print(f"  CLASS: {cls.__name__} | METHOD: {method_name}")
                                print(f"  ARGUMENTS: args={args}, kwargs={kwargs}")
                                print(f"  EXEC TIME: {duration:.6f} sec")
                                print(f"  RESULT:    {result}")

                    return method_wrapper

                setattr(cls, attr_name, make_wrapper(attr_name, attr_value))
        return cls

    return class_decorator


# ------- demo -------
@logger(show_magic_methods=True)
class Smart_type_value:
    """
    Допустим, у нас будет класс с "умной" типизацией (хочу складывать буквы и цифры)
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Smart({self.value})"

    def __add__(self, other):
        left = str(self.value)
        if isinstance(other, Smart_type_value):
            right = str(other.value)
        else:
            right = str(other)
            # or we work with exceptions or typeshifting if it's not Char or Numerical type
        return left + right

    def do_something(self):
        qwe = (2+2 == 4)
        print("[loggable class] not dunder method working")


silent = False
if __name__ == "__main__":
    print("[PROGRAM] creating obj 1")
    x = Smart_type_value(1)

    print("[PROGRAM] creating obj 2")
    y = Smart_type_value("1")

    print("[PROGRAM] working with given obj 1 and obj 2")
    print(y + x)

    print("[PROGRAM] do stuff with demo class object")
    x.do_something()
