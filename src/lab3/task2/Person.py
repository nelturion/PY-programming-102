class Person:
    def __init__(self, full_name: str, age: int):
        self.__full_name = full_name
        self.__age = age

    def get_age(self) -> int:
        return self.__age

    def get_name(self) -> str:
        return self.__full_name.split()[1]

    def get_surname(self) -> str:
        return self.__full_name.split()[0]

    def get_fathername(self) -> str:
        return self.__full_name.split()[2]

    def get_fullname(self) -> str:
        return self.__full_name

    #
    def formatted(self) -> str:
        return f"{self.__full_name} ({self.__age})"
