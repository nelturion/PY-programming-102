"""
Задание 3 - Скрипт для работы с системой.

Создайте скрипт на Python, который позволяет пользователю просматривать и управлять системными процессами, а также получать информацию о системном окружении.

Скрипт должен предоставлять интерактивное меню с следующими опциями:
a) Показать список всех запущенных процессов;
b) Показать детальную информацию о конкретном процессе;
c) Завершить процесс по его PID;
d) Показать и добавлять переменные окружения;
e) Изменить приоритет процесса;
f) Показать информацию о системе;
g) Выход.

Реализуйте обработку ошибок, например, для случаев, когда у пользователя нет прав на выполнение определенных операций.
"""

import os
import platform
import getpass
import psutil


def display_menu():
    print("\n" + "=" * 50)
    print("ИНТЕРАКТИВНОЕ МЕНЮ УПРАВЛЕНИЯ СИСТЕМОЙ")
    print("=" * 50)
    print("a) Показать список всех запущенных процессов")
    print("b) Показать детальную информацию о конкретном процессе")
    print("c) Завершить процесс по его PID")
    print("d) Показать и добавлять переменные окружения")
    print("e) Изменить приоритет процесса")
    print("f) Показать информацию о системе")
    print("g) Выход")
    print("=" * 50)


def show_all_processes():
    print(f"{'PID':<8} | {'Имя процесса':<30} | {'Статус':<15}")
    print("-" * 60)
    # Итерируемся по всем процессам, извлекая базовые атрибуты
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            info = proc.info
            print(f"{info['pid']:<8} | {info['name']:<30} | {info['status']:<15}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


def show_process_details():
    try:
        pid = int(input("Введите PID процесса: "))
        proc = psutil.Process(pid)

        print(f"\nДетальная информация о процессе {pid}:")
        print(f"Наименование: {proc.name()}")
        print(f"Статус:       {proc.status()}")
        print(f"Пользователь: {proc.username()}")
        print(f"Путь к файлу: {proc.exe()}")
        print(f"Потребление памяти: {proc.memory_info().rss / (1024 * 1024):.2f} MB")
    except ValueError:
        print("Ошибка: PID должен быть целым числом.")
    except psutil.NoSuchProcess:
        print(f"Ошибка: Процесс с PID {pid} не найден.")
    except psutil.AccessDenied:
        print("Ошибка: Отказано в доступе. Недостаточно прав для чтения данных процесса.")


def terminate_process():
    try:
        pid = int(input("Введите PID процесса для завершения: "))
        proc = psutil.Process(pid)
        proc.terminate()  # Посылает сигнал SIGTERM
        print(f"Сигнал на завершение процесса {pid} успешно отправлен.")
    except ValueError:
        print("Ошибка: PID должен быть целым числом.")
    except psutil.NoSuchProcess:
        print(f"Ошибка: Процесс с PID {pid} не найден.")
    except psutil.AccessDenied:
        print("Ошибка: Отказано в доступе. Требуются права администратора/sudo.")


def manage_env_variables():
    print("\nУправление переменными окружения:")
    print("1. Показать все переменные")
    print("2. Добавить/Изменить переменную")
    choice = input("Выберите действие (1-2): ").strip()

    if choice == "1":
        print(f"\n{'Переменная':<30} | {'Значение'}")
        print("-" * 60)
        for key, value in os.environ.items():
            # Ограничиваем длину значения для читаемости в консоли
            short_value = value[:50] + "..." if len(value) > 50 else value
            print(f"{key:<30} | {short_value}")
    elif choice == "2":
        key = input("Введите имя переменной: ").strip()
        value = input("Введите значение переменной: ").strip()
        if key:
            os.environ[key] = value
            print(f"Переменная {key} успешно установлена в текущем сеансе.")
        else:
            print("Ошибка: Имя переменной не может быть пустым.")
    else:
        print("Некорректный ввод.")


def change_priority():
    try:
        pid = int(input("Введите PID процесса: "))
        proc = psutil.Process(pid)

        print(f"Текущий приоритет: {proc.nice()}")
        print("Введите новое значение приоритета.")
        if platform.system() == "Windows":
            print("Допустимые значения: 64 (IDLE), 32 (NORMAL), 128 (HIGH), 256 (REALTIME)")
        else:
            print("Допустимые значения (nice): от -20 (наивысший) до 19 (наименьший)")

        new_priority = int(input("Новое значение: "))
        proc.nice(new_priority)
        print("Приоритет успешно изменен.")
    except ValueError:
        print("Ошибка: Введены некорректные числовые данные.")
    except psutil.NoSuchProcess:
        print(f"Ошибка: Процесс с PID {pid} не найден.")
    except psutil.AccessDenied:
        print("Ошибка: Отказано в доступе. Изменение приоритета требует повышенных прав.")


def show_system_info():
    print("\nИНФОРМАЦИЯ О СИСТЕМЕ:")
    print(f"Операционная система: {platform.system()} {platform.release()}")
    print(f"Архитектура:          {platform.machine()}")
    print(f"Имя хоста:            {platform.node()}")
    print(f"Текущий пользователь: {getpass.getuser()}")
    print(f"Количество ядер CPU:  {psutil.cpu_count(logical=True)}")

    virtual_mem = psutil.virtual_memory()
    print(f"Оперативная память:   {virtual_mem.used / (1024 ** 3):.2f} GB из {virtual_mem.total / (1024 ** 3):.2f} GB")


def system_manager():
    while True:
        display_menu()
        choice = input("Выберите пункт меню (a-g): ").strip().lower()

        if choice == 'a':
            show_all_processes()
        elif choice == 'b':
            show_process_details()
        elif choice == 'c':
            terminate_process()
        elif choice == 'd':
            manage_env_variables()
        elif choice == 'e':
            change_priority()
        elif choice == 'f':
            show_system_info()
        elif choice == 'g':
            print("Завершение работы скрипта.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, введите букву от 'a' до 'g'.")


if __name__ == "__main__":
    system_manager()