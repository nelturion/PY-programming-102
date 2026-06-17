"""
Задание 2 - Скрипт для работы с директориями.

Реализуйте скрипт который:
1) Скопирует файл с предыдущего задания;
2) Переименует файл. Создайте несколько вложенных директорий и переместите копию файла в одну из них;
3) Создаст новый файл. Переместите и переименуйте его с помощью одной команды os;
4) Программно создайте ещё несколько файлов. Выведите все файлы и директории, лежащие в папке, в которой запущен скрипт.
Переместитесь во вложенную директорию в которую переместили файл. Выведите все, что находится в этой директории;
5) Вернитесь в папку со скриптом; Создайте пустую директорию, после чего удалите её. Создайте ещё несколько вложенных директорий и файлов;
6) Обойдите текущую директорию и выведите: путь до каждой папки, список файлов в каждой папке.
"""

import os
import shutil


def directory_operations():
    print("--- Начинаем работать с директориями ---")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Гарантируем наличие исходного файла из Задания 1
    source_file = "lab3_t1_test_subject.txt"
    if not os.path.exists(source_file):
        with open(source_file, "a", encoding="utf-8") as f:
            f.write("base data")

    # 1. Скопирует файл с предыдущего задания;
    copied_file = "copy_t1.txt"    # файлы нельзя называть одинаково, поэтому уже на этапе создания копии мы переименовываем l3_t1_test_sbj в copied_sbj
    shutil.copy(source_file, copied_file)
    print(f"1) Файл скопирован в {copied_file}")

    # 2. Переименует файл.
    renamed_file = "rename_t2.txt"
    os.rename(copied_file, renamed_file)

    # Создайте несколько вложенных директорий и переместите копию файла в одну из них;
    nested_dir = os.path.join("nested_1", "nested_2", "nested_3")
    os.makedirs(nested_dir, exist_ok=True)
    target_path_1 = os.path.join(nested_dir, renamed_file) # перемещаем rename_t2 на дно nested
    os.rename(renamed_file, target_path_1)
    print(f"2) Переименован и перемещен в {target_path_1}\n")

    # 3. Создаст новый файл.
    temp_new_file = "temp_t3.txt"  # создали новое имя файла
    with open(temp_new_file, "a", encoding="utf-8") as f:   # определили что это имя файла будет файлом
        f.write("t3 data") # файл без данных не файл (мы в принципе можем убрать "new data" оставить pass)

    # Переместите и переименуйте его с помощью одной команды os;
    final_path_3 = os.path.join("nested_1", "renamed_t3.txt") # создаем новый путь      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    os.rename(temp_new_file, final_path_3) # одной командой сделали 2 дела (ну как mv в линуксе)
    print(f"3) Создали и переместили (переименовали) третий файл в {final_path_3}")

    # 4. Программно создайте ещё несколько файлов.
    for i in range(1, 4):
        with open(f"extra_t4_{i}.txt", "a", encoding="utf-8") as f:
            f.write(f"t4 extra data {i}")

    # Выведите все файлы и директории, лежащие в папке, в которой запущен скрипт.
    print(f"\n4) Содержимое папки со скриптом {os.getcwd()}: ")
    print(os.listdir("."))

    # Переместитесь во вложенную директорию в которую переместили файл. Выведите все, что находится в этой директории;
    os.chdir("./nested_1")
    print(f"\nСодержимое вложенной папки {os.getcwd()}: ")
    print(os.listdir("."))

    # 5. Вернитесь в папку со скриптом;
    os.chdir(script_dir)
    print(f"\nВернулись в папку со скриптом {os.getcwd()}")

    # Создайте пустую директорию, после чего удалите её.
    empty_dir = "temp_empty_dir"
    os.mkdir(empty_dir)
    print(f"\nСодержимое папки со скриптом {os.getcwd()} (существует временная папка): ")
    print(os.listdir("."))
    os.rmdir(empty_dir)

    # Создайте ещё несколько вложенных директорий и файлов;
    another_nested = os.path.join("t5_A", "t5_B", "t5_C")
    os.makedirs(another_nested, exist_ok=True)
    with open(os.path.join(another_nested, "t5_file_1.txt"), "a") as f:
        pass    # пусть он будет в t5_C
    with open(os.path.join("t5_A", "t5_B", "t5_file_2.txt"), "a") as f:
        pass    # этот будет в t5_B

    # 6. Обойдите текущую директорию и выведите: путь до каждой папки, список файлов в каждой папке.
    print("\n(: sudo apt install tree\ntree")
    for root, dirs, files in os.walk("."):
        print(f"Папка: {root}\n")
        print("  файлы:", ", ".join(files))

    return script_dir


if __name__ == "__main__":
    directory_operations()