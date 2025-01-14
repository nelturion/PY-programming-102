class Movie:
    def __init__(self, movie_id: int, views: int = 0):
        self.__movie_id = movie_id
        self.__views = views
        self.__title = ""

    def get_id(self) -> int:
        return self.__movie_id

    @staticmethod
    def get_title(movie_id: int) -> str:
        '''
        Linear search for name in movie_list

        @returns a title of a movie by id
        '''
        with (open("../resources/txt/movie_list.txt", "r", encoding="utf-8") as file):
            for line in file.readlines():
                line_as_list = line.rstrip().split(",")
                if int(line_as_list[0]) == movie_id:
                    title = line_as_list[1]
        return title

    def get_views(self) -> int:
        '''
        Returns amount of views of this movie by all viewers (users)
        '''
        # у это если прям совсееееееееем симулировать создание сервиса
        with open("../resources/txt/watch_history.txt", "r", encoding="utf-8") as file:
            i = 0
            views = 0
            for line in file.readlines():
                i += 1
                for j in [int(el) for el in line.split(",")]:
                    if j == self.get_id():
                        views += 1
        self.__views = views
        return self.__views

    def get_unique_views(self) -> int:
        with open("../resources/txt/watch_history.txt", "r", encoding="utf-8") as file:
            unique_views = 0
            for line in file.readlines():
                if line.__contains__(str(self.get_id())):
                    unique_views += 1
        return unique_views

