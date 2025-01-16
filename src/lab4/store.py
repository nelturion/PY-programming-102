import re
from collections import defaultdict


def validate_phone(phone: str) -> tuple[bool, str] | str:
    """
    Функция валидации номера телефона. Паттерн "+?-???-???-??-??" считается исключительно верным.
    :param phone: Номер телефона в формате строки.
    :return: Tuple(валидность номера и сам номер) или строку с предупреждением
    >>> validate_phone("+7-101-123-45-67")
    (True, '+7-101-123-45-67')
    >>> validate_phone("")
    (False, 'no data')
    >>> validate_phone("+123-456-789")
    (False, 'invalid format')
    """
    if phone == "":
        return False, "no data"
    pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'  # Проверяем номер с помощью регулярных выражений. Потому что так надо.
    return bool(re.match(pattern, phone)), phone if re.match(pattern, phone) else "invalid format"


def validate_address(address: str) -> tuple[bool, str] | str:
    """
    Валидация адреса доставки.
    :param address: Адрес доставки
    :return: Tuple(валидность адреса и сам адрес) или строка с предупреждением.
    >>> validate_address("")
    (False, 'no data')
    >>> validate_address("Россия. Краснодарский край. Сочи. Проспект Ленина.")
    (False, 'invalid format')
    >>> validate_address("Россия. Краснодарский край. Сочи. Проспект Ленина")
    (True, 'Россия. Краснодарский край. Сочи. Проспект Ленина')
    """
    if address == "":
        return False, "no data"
    pattern = r'^.+?\.\s+.+?\.\s+.+?\.\s+[^.]+$' # r'^[^;]+\. [^;]+\. [^;]+\. [^;]+$'  # опять таки regex, потому что так надо.
    return bool(re.match(pattern, address)), address if re.match(pattern, address) else "invalid format"

def process_orders(file_path: str) -> tuple[list, list]:
    """
    Обработка списка заказов.
    :param file_path: Путь к файлу со списком заказов.
    :return: Два списка: список валидных заказов и список невалидных заказов.
    """
    valid_orders = []
    invalid_orders = []

    # Считывание файла с заказами
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            order_id, products, full_name, address, phone, priority = line.strip().split(';')

            # Валидация адреса
            address_valid, address_error = validate_address(address)
            if not address_valid:
                invalid_orders.append(f"{order_id};1;{address_error}")  # добавляем в список с валидными адресами

            # Валидация телефона
            phone_valid, phone_error = validate_phone(phone)
            if not phone_valid:
                invalid_orders.append(f"{order_id};2;{phone_error}")  # добавляем в список с валидными телефонами

            # Если нет ошибок, добавляем заказ в общий список
            if address_valid and phone_valid:
                products_counted = defaultdict(int)  # создаем словарь, где любое новое знаечение
                                                     # будет проинициализировано нулем
                for product in products.split(', '):
                    products_counted[product] += 1

                formatted_products = ', '.join([f"{prod} x{count}" for prod, count in products_counted.items()])
                country = address.split('.')[0].strip()
                region_city_street = '. '.join(address.split('.')[1:]).strip()

                valid_orders.append(
                    (country, priority, order_id, formatted_products, full_name, region_city_street, phone))

    # Сортировка валидных заказов по стране и приоритету. Первыми в списке идут заказы из России
    priority_order = {'MAX': 1, 'MIDDLE': 2, 'LOW': 3}
    valid_orders.sort(key=lambda x: (x[0] != 'Россия', priority_order[x[1]]))

    # Сохранение валидных заказов
    validated_orders = []
    for order in valid_orders:
        country, priority, order_id, products_formatted, full_name, region_city_street, phone = order
        validated_orders.append( (order_id, products_formatted, full_name, region_city_street, phone, priority) )

    return validated_orders, invalid_orders


def write_valid_orders(valid_orders: list, output_file: str) -> None:
    """
    Записывает валидные заказы в файл. Заказы должны быть предварительно отсортированы.
    :param valid_orders: Список заказов валидированых и форматированых
    :param output_file: Путь к файлу, где будут храниться эти заказы.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        for order in valid_orders:
            order_id, products_formatted, full_name, region_city_street, phone, priority = order
            file.write(f"{order_id};{products_formatted};{full_name};{region_city_street};{phone};{priority}\n")


def write_invalid_orders(invalid_orders: list, output_file: str) -> None:
    """
    Запись невалидных заказов в файл.
    :param invalid_orders: Список невалидных заказов
    :param output_file: Путь к файлу
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        for invalid_order in invalid_orders:
            file.write(f"{invalid_order}\n")


if __name__ == '__main__':
    valid_orders, invalid_orders = process_orders("resources/orders.txt")
    write_invalid_orders(invalid_orders, "resources/invalid_orders.txt")
    write_valid_orders(valid_orders, "resources/valid_orders.txt")

