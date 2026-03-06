from src.sem1.lab3.task2.Person import Person


class Group:
    def __init__(self, min_age: int, max_age: int, unique_property: bool = False):
        self.__max = max_age
        self.__min = min_age
        self.__unique_property = unique_property
        self.persons = []

    '''
    def print_ages(self):
        print(f"{self.__min}-{self.__max}")
    '''

    def get_ages(self) -> tuple[int, int]:
        return self.__min, self.__max

    def get_ages_str(self) -> str:
        if self.__unique_property:
            return f"{self.__min}+"
        return f"{self.__min}-{self.__max}"

    def add_person(self, person: Person):
        self.persons.append(person)

    def is_empty(self) -> bool:
        if len(self.persons) == 0:
            return True
        else:
            return False

    def get_sorted_persons(self):
        # self.__persons.sort(key=lambda x: (x.get_age(), x.get_fullname()))
        return sorted(self.persons, key=lambda x: (-x.get_age(), x.get_fullname()))  #

    def sort_persons(self):
        self.persons.sort(key=lambda x: (-x.get_age(), x.get_fullname()))

    def get_persons(self) -> list[Person]:
        # self.sort_persons_in_group()
        return self.persons  # self.get_sorted_persons()
