class User:
    '''
    User class with parameters: user_id, history, and optional - username
    '''
    __default_name = "Username"

    def __init__(self, id: int, history: list, name: str = __default_name):
        self.__id = id
        self.__name = name
        self.__history = history

    def get_id(self) -> int:
        return self.__id

    def get_user_name(self) -> str:
        '''
        returns name of a user
        '''
        return self.__name

    def get_history(self) -> list:
        '''
        returns a list history containing / Полная история просмотров
        '''
        return self.__history

    ############################ useless stuff goes here: ############################
    def new_view(self, movie_id: int):
        '''
        Adds a new view in user's view history
        @param movie_id stands for movie id (obviously)
        '''
        self.__history.append(movie_id)

    @staticmethod
    def __get_user_amount(history_file: str) -> int:
        with open(history_file, "r") as file:
            return len(file.readlines())

    def get_unique_views(self) -> list[int]:
        '''
        Returns a list of unique views for selected user / Просмотренные фильмы
        '''
        views = set(self.get_history())
        return sorted(list(views))
