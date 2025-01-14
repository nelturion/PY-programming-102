import random
import random as r


def generate_history(min_story_len: int = 1, max_story_len: int = 10, user_amount: int = 10):
    with open("../resources/txt/watch_history.txt", "w") as file:
        for j in range(user_amount):
            lst = []
            story_len = random.randint(min_story_len, max_story_len)
            for i in range(story_len):
                lst.append(str(r.randint(1, 9)))
            s = ",".join(lst)
            file.writelines(s)
            file.write("\n")


if __name__ == "__main__":
    generate_history(3, 15, 100)
