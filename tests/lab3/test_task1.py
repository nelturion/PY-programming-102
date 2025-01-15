import unittest
from src.lab3.task1.Recommendation_System import Recommendation_System
from src.lab3.task1.User import User


class test_task1(unittest.TestCase):
    def test_isSimilar(self):
        test_feed = Recommendation_System(User(1, []), [[1,2,3,4], [1,2,3,4,5,6,7,8,9]])

        history1 = [1, 2, 3, 4]
        history2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result1 = test_feed.is_similar(history1, history2)
        self.assertTrue(result1)

        history1 = [1, 2, 3, 4, 5]
        history2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result2 = test_feed.is_similar(history1, history2)
        self.assertTrue(result2)

        history1 = []
        history2 = []
        result3 = test_feed.is_similar(history1, history2)
        self.assertTrue(result3)

        history1 = [1, 2, 3]
        history2 = [4, 5, 6]
        result4 = test_feed.is_similar(history1, history2)
        self.assertFalse(result4)

        history1 = [1, 2, 3]
        history2 = [3, 4, 5]
        result5 = test_feed.is_similar(history1, history2)
        self.assertFalse(result5)

        history1 = [1, 2]
        history2 = [1, 2, 3, 4]
        result6 = test_feed.is_similar(history1, history2)
        self.assertTrue(result6)

        history1 = [1, 2, 3, 4, 5, 6]
        history2 = [1, 2, 3, 4]
        result7 = test_feed.is_similar(history1, history2)
        self.assertTrue(result7)

        history1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        history2 = [1, 2, 3, 4]
        result8 = test_feed.is_similar(history1, history2)
        self.assertFalse(result8)

    def setUp(self):
        self.user1 = User(1, [1, 2, 3, 4])
        self.user2 = User(2, [1, 2, 3, 4, 5])
        self.user3 = User(3, [])
        self.user4 = User(4, [1, 2, 3])
        self.user5 = User(5, [1, 2, 3])
        self.user6 = User(6, [1, 2])
        self.subject_user1 = User(7, [1, 2])
        self.subject_user2 = User(8, [3])
        self.subject_user3 = User(9, [100])

        self.users = [self.user1, self.user2, self.user3, self.user4, self.user5, self.user6]
        self.history_file = [usr.get_history() for usr in self.users]

    def test_get_similar_by_history(self):
        # given
        # setUp()

        # when
        test_feed = Recommendation_System(self.subject_user1, self.history_file)
        similars1 = [self.user1, self.user2, self.user4, self.user5, self.user6]

        test_feed2 = Recommendation_System(self.subject_user2, self.history_file)
        similars2 = [self.user1, self.user2, self.user4, self.user5]

        test_feed3 = Recommendation_System(self.subject_user3, self.history_file)
        similars3 = []

        # then
        self.assertListEqual(similars1, test_feed.get_similar_by_history(self.users))
        self.assertListEqual(similars2, test_feed2.get_similar_by_history(self.users))
        self.assertListEqual(similars3, test_feed3.get_similar_by_history(self.users))

    def test_exclude_viewed(self):
        # given
        test_feed1 = Recommendation_System(self.subject_user1, self.history_file)
        test_feed2 = Recommendation_System(self.subject_user2, self.history_file)
        test_feed3 = Recommendation_System(self.subject_user3, self.history_file)

        similars1 = test_feed1.get_similar_by_history(self.users)
        similars2 = test_feed2.get_similar_by_history(self.users)
        similars3 = test_feed3.get_similar_by_history(self.users)

        suggestions_for_1 = test_feed1.exclude_viewed(similars1)
        suggestions_for_2 = test_feed2.exclude_viewed(similars2)
        suggestions_for_3 = test_feed3.exclude_viewed(similars3)

        # when
        real_suggestions1 = [3, 4, 5]
        real_suggestions2 = [1, 2, 4, 5]
        real_suggestions3 = []

        # then
        self.assertSetEqual({el for _ in suggestions_for_1 for el in _}, set(real_suggestions1))
        self.assertSetEqual({el for _ in suggestions_for_2 for el in _}, set(real_suggestions2))
        self.assertSetEqual({el for _ in suggestions_for_3 for el in _}, set(real_suggestions3))

    def test_sort_by_most_viewed_from_list(self):
        #given
        test_feed1 = Recommendation_System(self.subject_user1, self.history_file)
        test_feed2 = Recommendation_System(self.subject_user2, self.history_file)
        test_feed3 = Recommendation_System(self.subject_user3, self.history_file)

        similars1 = test_feed1.get_similar_by_history(self.users)
        similars2 = test_feed2.get_similar_by_history(self.users)
        similars3 = test_feed3.get_similar_by_history(self.users)

        suggestions_for_1 = test_feed1.exclude_viewed(similars1)
        suggestions_for_2 = test_feed2.exclude_viewed(similars2)
        suggestions_for_3 = test_feed3.exclude_viewed(similars3)

        sorted_suggestions1 = test_feed1.sort_by_most_viewed_from_list(suggestions_for_1)
        sorted_suggestions2 = test_feed2.sort_by_most_viewed_from_list(suggestions_for_2)
        sorted_suggestions3 = test_feed3.sort_by_most_viewed_from_list(suggestions_for_3)

        #when
        real_sorted1 = [3, 4, 5]
        real_sorted2 = [1, 2, 4, 5]
        real_sorted3 = []

        #then
        self.assertListEqual(real_sorted1, sorted_suggestions1)
        self.assertListEqual(real_sorted2, sorted_suggestions2)
        self.assertListEqual(real_sorted3, sorted_suggestions3)
