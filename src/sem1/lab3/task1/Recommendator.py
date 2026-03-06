from src.sem1.lab3.task1.Recommendation_System import Recommendation_System
from src.sem1.lab3.task1.User import User
from src.sem1.lab3.task1.Movie import Movie


def generate_new_id():
    with open("../resources/txt/watch_history.txt", "r", encoding="utf-8") as file:
        return len(file.readlines())


if __name__ == "__main__":
    inp = input("Input your watch history: ")
    new_user_history = [int(el) for el in inp.split(",")]  # 2,4,1,1

    # append inputs to the watch_history file
    with open("../resources/txt/watch_history.txt", "a") as file:
        s = ",".join(inp.split(","))
        file.write("\n")
        file.write(s)

    # create new user with his (this program's) own instance of Recommendation_System(based on his history)
    my_feeder = Recommendation_System(User(generate_new_id(), new_user_history, "GoodTragedian"),
                                      "../resources/txt/watch_history.txt")

    # generate recommendation
    movie_id = my_feeder.get_next_recommendation(0)
    name = Movie.get_title(movie_id)  # :thinkingface: вызывать статический метод другого класса
    print(f"{name}")
