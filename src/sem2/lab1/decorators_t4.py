from functools import wraps


def call_limiter(limit):
    """
        Задание 4 - декоратор класса с параметром:
        Реализовать декоратор call_limiter(limit), который ограничивает вызов каждого метода, позволяя вызвать их limit раз.

        >>> @call_limiter(limit=2)
        ... class Courier:
        ...     def deliver(self):
        ...         return "Package delivered!"

        >>> obj = Courier()
        >>> obj.deliver()
        'Package delivered!'
        >>> obj.deliver()
        'Package delivered!'
        >>> obj.deliver()
        Traceback (most recent call last):
        ValueError: Method deliver has exceeded its call limit of 2.
        """

    def class_decorator(cls):
        # Перебираем все атрибуты класса
        for attr_name, attr_value in list(cls.__dict__.items()):

            # Проверяем, что это метод и он не магический
            if callable(attr_value) and not (attr_name.startswith("__") and attr_name.endswith("__")):

                def make_limited_method(original_method, method_name):
                    @wraps(original_method)
                    def method_wrapper(self, *args, **kwargs):
                        # Создаем уникальный ключ для счетчика этого метода в объекте
                        counter_attr = f"_calls_amount_{method_name}"

                        # Если метода еще не было в словаре объекта, ставим 0
                        if not hasattr(self, counter_attr):
                            setattr(self, counter_attr, 0)

                        # Получаем текущее число вызовов
                        current_calls = getattr(self, counter_attr)

                        if current_calls >= limit:
                            raise ValueError(f"Method {method_name} has exceeded its call limit of {limit}.")

                        # Инкрементируем счетчик и вызываем оригинальный метод
                        setattr(self, counter_attr, current_calls + 1)
                        return original_method(self, *args, **kwargs)

                    return method_wrapper

                # Заменяем оригинальный метод на нашу лимитированную обертку
                setattr(cls, attr_name, make_limited_method(attr_value, attr_name))

        return cls

    return class_decorator


# ------ demo ------

@call_limiter(limit=2)
class SmartLamp:
    def __init__(self, location):
        self.location = location

    def turn_on(self):
        print(f"[{self.location}] Лампа включена")

    def change_color(self, color):
        print(f"[{self.location}] Цвет изменен на {color}")


if __name__ == "__main__":
    print("=== Старт демонстрации декоратора call_limiter ===")

    # 1. Создаем первый объект (Лампа в спальне)
    bedroom_lamp = SmartLamp("Спальня")

    print("\n--- Проверяем работу первого объекта (Лимит = 2) ---")
    bedroom_lamp.turn_on()  # Вызов 1 — Ок
    bedroom_lamp.turn_on()  # Вызов 2 — Ок

    try:
        bedroom_lamp.turn_on()  # Вызов 3 — Должен вызвать ошибку!
    except ValueError as e:
        print(e)

    # 2. Проверяем другой метод этой же лампы
    print("\n--- Проверяем другой метод того же объекта (Счетчики раздельные) ---")
    bedroom_lamp.change_color("Красный")  # Вызов 1 — Ок (так как лимит считается для каждого метода отдельно)

    # 3. Создаем второй объект (Лампа на кухне)
    print("\n--- Проверяем изоляцию объектов (Новый объект = новые лимиты) ---")
    kitchen_lamp = SmartLamp("Кухня")

    # Если бы счетчик был один на класс, тут бы сразу вылетела ошибка.
    # Но так как счетчики хранятся внутри каждого self, всё сработает идеально
    kitchen_lamp.turn_on()  # Вызов 1 для кухни — Ок
    kitchen_lamp.turn_on()  # Вызов 2 для кухни — Ок

    print("\n=== Демонстрация успешно завершена! ===")
