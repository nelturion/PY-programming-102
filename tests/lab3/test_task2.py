import unittest

from src.lab3.task2.Group import Group
from src.lab3.task2.Person import Person


class test_task1(unittest.TestCase):
    def setUp(self):
        self.person1 = Person("a", 15)
        self.person2 = Person("a", 15)
        self.person3 = Person("a", 15)

    def test_is_empty(self):
        # given
        group = Group(0, 100)
        group.add_person(self.person1)
        group.add_person(self.person2)
        group.add_person(self.person3)

        group2 = Group(100, 123)

        # when
        res = group.is_empty()
        res2 = group2.is_empty()

        # then
        self.assertFalse(res)
        self.assertTrue(res2)
