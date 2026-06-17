"""
Задание 1 - Скрипт для работы с файлами. Всё необходимо выполнять с помощью библиотеки os. Запрещается использовать cmd
или иные средства. Проверьте в какой директории выполняется скрипт. Если оказалось, что исполняемая директория не та, в
которой лежит скрипт, то переместитесь туда.

Реализуйте скрипт который:
1) Создает файл;
2) Запишет в него любые адекватные данные. С помощью библиотеки os проверьте, что файл существует, при этом запрещается
писать пути руками (но дописывать пути разрешается);
3) Выведет размер файла в байтах, дату последнего изменения, дату последнего доступа к этому файлу;
4) Выведет текущего пользователя;
5) Посмотрите уровень доступа к этому файлу. Поменяйте права доступа к нему. Проверьте, что у вас всё получилось.

небольшая справка по правам:
7 - rwx
6 - rw
4 - r
user(owner) | group | others
"""

import os
import getpass
from datetime import datetime

def file_operations():
    print("--- Старт работы с файловой системой ---")

    # 0. Проверка и смена директории
    script_dir = os.path.dirname(os.path.abspath(__file__))
    current_dir = os.getcwd()

    print(f"Директория скрипта:       {script_dir}")
    print(f"Директория где мы сейчас: {current_dir}")

    if current_dir != script_dir:
        os.chdir(script_dir)
        print(f"-->переместились в директорию скрипта: {script_dir}")

    # 1. Создаем файл
    filename = "lab3_t1_test_subject.txt"
    file_path = os.path.join(script_dir, filename)  # это полное название
        # вот тут можно добавить защиту от падения на ровном месте (проверкой и принудительной выдачей права на редактирование)
    with open(file_path, "w", encoding="utf-8") as f: # создали и открыли
        f.write("example data") # записали что-то

    # 2. создан? солипсист?
    if os.path.exists(file_path):
        print(f"\nФайл успешно создан: {file_path}")

    # 3. когда, сколько байт и можно ли его потрогать?
    file_stat = os.stat(file_path)
    file_size = file_stat.st_size

    last_modify_time = datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    last_access_time = datetime.fromtimestamp(file_stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")

    print(f"\nРазмер файла: {file_size} байт")
    print(f"Дата последнего изменения: {last_modify_time}")
    print(f"Дата последнего доступа: {last_access_time}")

    # 4. кто здесь?
    current_user = getpass.getuser()
    print(f"\nТекущий пользователь: {current_user}")

    # 5. какие права у тебя есть?
        # и соответственно обновить наши знания про файл, так как мы уже могли поменять права или еще что-то
        # file_stat = os.stat(file_path)
    current_mode = file_stat.st_mode & 0o777
    print(f"\nПрава доступа (октально): {oct(current_mode)}")

    # попробуем поменять права
    print("Теперь у вас (возможно) будут права 'Только для чтения' (0o444)...")
    os.chmod(file_path, 0o444)

    # поменялось?
    new_stat = os.stat(file_path)
    new_mode = new_stat.st_mode & 0o777
    if new_mode == 0o444:
        print("Успешно изменены права доступа на 0o444!")
    print(f"Нынешние права доступа (октальные): {oct(new_mode)}")

    # ладно, откатываем права назад
    print("\nоткат откат откат откат откат ctrl+z")
    os.chmod(file_path, 0o666)
    rollback_stat = os.stat(file_path)
    rollback_mode = rollback_stat.st_mode & 0o777
    if rollback_mode == 0o666:
        print("Успешно восстановлены права доступа на 0o666!")
    print(f"Нынешние права доступа (октальные): {oct(rollback_mode)}")
    return file_path

if __name__ == "__main__":
    file_operations()