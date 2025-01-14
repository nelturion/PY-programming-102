import sys
from Group import Group
from Person import Person


def generate_groups(string_args: list[int]):
    groups = []
    min_age = 0
    max_age = 123
    for i in range(len(string_args) + 1):
        if i < len(string_args):
            max_age = string_args[i]
            groups.append(Group(min_age, max_age))
            min_age = string_args[i] + 1
        else:
            groups.append(Group(min_age, 123, True))
    return groups


if __name__ == "__main__":
    groups = generate_groups([int(arg) for arg in sys.argv[1:]])
    persons = []
    while True:
        s = input()
        if s == "END":
            break
        name, age = s.split(",")
        persons.append(Person(name, age))

    # split persons into groups
    for group in groups:
        for person in persons:
            if int(person.get_age()) in range(*group.get_ages()):
                group.add_person(person)

    # result output
    for group in reversed(groups):
        if not group.is_empty():
            print(f"{group.get_ages_str()}: {", ".join([person.formatted() for person in group.get_persons()])}")



