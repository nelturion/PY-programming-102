import math

from src.lab3.task1 import User


class Recommendation_System(User.User):
    def __init__(self, user: User.User, history_file: str | list[list[int]] = "../resources/txt/watch_history.txt"):
        super().__init__(user.get_id(), user.get_history())
        if isinstance(history_file, str):
            self.__users = self.__user_assignment(history_file)
        elif isinstance(history_file, list):
            self.__users = history_file

    @staticmethod
    def __user_assignment(history_file: str) -> list[User.User]:
        users = []
        with open(history_file, "r") as file:
            i = 0
            for line in file.readlines():
                story = [int(el) for el in line.rstrip().split(",")]
                users.append(User.User(i, story))
                i += 1
        return users

    @staticmethod
    def is_similar(hist1: list[int], hist2: list[int]) -> bool:
        '''
        Check whether the histories are similar (similar interests?)
        Заданной будем считать hist1. Сравниваем заданную с чужой.
        >>> test_user = User.User(1,[])
        >>> test_feed = Recommendation_System(test_user, "../resources/txt/watch_history.txt")
        >>> test_feed.is_similar([1,2,3,2,1], [3,2,7,6])
        True
        >>> test_feed.is_similar([],[])
        True
        >>> test_feed.is_similar([1,2,3],[4,5,6])
        False
        >>> test_feed.is_similar([1,2,3], [3,4,5])
        False
        >>> test_feed.is_similar([1,2], [1,2,3,4])
        True
        >>> test_feed.is_similar([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        True
        >>> test_feed.is_similar([1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4])
        False
        '''

        cnt_in = 0  # считаем сколько элементов внутри списка 1 лежат внутри списка 2
        for el in hist1:
            if el in hist2:
                cnt_in += 1

        if cnt_in >= math.ceil(len(set(hist1)) / 2):  # "хотя бы половина фильмов совпадает с заданной" (1/3 < 0.5)
            return True
        else:
            return False

    def get_similar_by_history(self, userlist: list[User.User]) -> list[User.User]:
        '''
        Возвращает список юзеров с похожими историями просмотров
        '''
        similars = []
        for user in userlist:
            if self.is_similar(self.get_history(), user.get_history()):
                similars.append(user)
        return similars

    def exclude_viewed(self, similar_users: list[User.User]) -> list[list[int]]:
        '''
        Возвращает истории без повторений просмотров
        '''
        similars = similar_users  #self.get_similar_by_history(self.__users)  # 1.берем похожих
        suggestions = []
        for user in similars:
            # а что из списка просмотренного user-ами наш челик не посмотрел?
            new_sim = list(set(user.get_history()).difference(set(self.get_history())))  # 2.исключаем
            suggestions.append(new_sim)
        return suggestions

    @staticmethod
    def sort_by_most_viewed_from_list(watch_list: list[list[int]]) -> list[int]:
        view_counter = {}
        for sublist in watch_list:
            for view in sublist:
                if view in view_counter:
                    view_counter[view] += 1  # пусть это будет словарь вида - {какой фильм: сколько раз посмотрели}
                else:
                    view_counter[view] = 1

        return sorted(view_counter, key=view_counter.get, reverse=True)

    def get_recommended_list(self) -> list[int]:
        '''
        Генерирует рекомендацию основываясь на похожих историях юзеров
        '''
        similars = self.exclude_viewed(self.get_similar_by_history(self.__users))
        return self.sort_by_most_viewed_from_list(similars)

    def get_next_recommendation(self, recommendation_cntr: int) -> int:
        return self.get_recommended_list()[recommendation_cntr]
