import sys
import importlib
from Group import Group
from Person import Person


def generate_groups(argv: list[int]) -> list[Group]:
    groups = []
    min_age = 0
    max_age = 123
    for i in range(len(argv) + 1):
        if i < len(argv):
            max_age = argv[i]
            groups.append(Group(min_age, max_age))
            min_age = argv[i] + 1
        else:
            groups.append(Group(min_age, 123, True))
    return groups


def generate_persons(file_path: str) -> list[Person]:
    persons = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            name, age = line.rstrip().split(",")
            persons.append(Person(name, int(age)))   ## Python - это нерабочий криндж.
    return persons


if __name__ == "__main__":  # 18, 25, 35, 45, 60,

    sample_argv = [80, 100]

    # sample_argv = [int(arg) for arg in sys.argv[1:]]
    sample_persons = "../resources/txt/names.txt"

    groups = generate_groups(sample_argv)
    persons = generate_persons(sample_persons)

    # split people into groups
    for group in groups:
        for person in persons:
            if int(person.get_age()) in list(range(*group.get_ages())):
                group.add_person(person)

    for group in groups:
        group.persons.sort(key=lambda x: (-x.get_age(), x.get_fullname()))


    # result output
    for group in reversed(groups):
        if not group.is_empty():
            print(f"{group.get_ages_str()}: {", ".join([person.formatted() for person in group.get_persons()])}")
