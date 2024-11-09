"""
This code implements methods of Vigenre encryption and decryption algorithm.
А еще можно его протестить, если просто запустить модуль вручную. Вооооот...
"""
import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    #>>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    #>>> encrypt_vigenere("python", "a")
    'python'
    #>>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    #>>> encrypt_vigenere("AttackAtDawn", "lemon")
    'LxfopvEfRnhr'
    """
    ciphertext = ""

    # create alphabet of both upper and lower case letters
    lower_chars = dict(enumerate(list(string.ascii_lowercase)))
    inverted_lower_chars = {v: k for k, v in lower_chars.items()}
    upper_chars = dict(enumerate(list(string.ascii_uppercase)))
    inverted_upper_chars = {v: k for k, v in upper_chars.items()}

    key = full_and_even_key(plaintext, keyword)  # дополняем keyword до длины слова

    # получаем индексы букв КЛЮЧА и СЛОВА в алфавите
    key_letter_nums = [str(inverted_upper_chars[ch]) if ch.isupper() else inverted_lower_chars[ch] for ch in key]
    word_letter_nums = [str(inverted_upper_chars[ch]) if ch.isupper() else inverted_lower_chars[ch] for ch in plaintext]

    # создаем массив в котором будут храниться алфавитные номера букв согласно алгоритму Виженера
    enc_letters_list = []
    for a, b in zip(word_letter_nums, key_letter_nums):  # итерируемся по индексам' из обоих списков КЛЮЧА и СЛОВА
        enc_letters_list.append(
            str((int(a) + int(b)) % 26) if isinstance(a, str) else (a + b) % 26
        )

    # создаем строку из алфавитных номеров полученных символов
    ciphertext = "".join(
        upper_chars[int(element)] if isinstance(element, str) else lower_chars[element] for element in enc_letters_list
    )
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    #>>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    #>>> decrypt_vigenere("python", "a")
    'python'
    #>>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    #>>> decrypt_vigenere("LxfopvEfRnhr", "LeMoN")
    'AttackAtDawn'
    """
    plaintext = ""

    # create alphabet of both upper and lower case letters
    lower_chars = dict(enumerate(list(string.ascii_lowercase)))
    inverted_lower_chars = {v: k for k, v in lower_chars.items()}
    upper_chars = dict(enumerate(list(string.ascii_uppercase)))
    inverted_upper_chars = {v: k for k, v in upper_chars.items()}

    keyword = full_and_even_key(ciphertext, keyword)  # дополняем keyword до длины слова

    # получаем индексы букв КЛЮЧА и СЛОВА в алфавите
    key_letter_nums = [str(inverted_upper_chars[ch]) if ch.isupper() else inverted_lower_chars[ch] for ch in keyword]
    word_letter_nums = [
        str(inverted_upper_chars[ch]) if ch.isupper() else inverted_lower_chars[ch] for ch in ciphertext
    ]

    # создаем массив в котором будут храниться алфавитные номера букв согласно алгоритму Виженера
    enc_letters_list = []
    for a, b in zip(word_letter_nums, key_letter_nums):
        if isinstance(a, str):
            a = int(a)
            b = int(b)
            x = str(a - b if a - b >= 0 else 26 - abs(a - b))
        else:
            # гугля, как можно было бы это реализовать по-другому, я пришел к идее использовать
            # отрицательный индекс для list(lower_chars.values()); реализовывать не стал.
            x = a - b if a - b >= 0 else 26 - abs(a - b)
        enc_letters_list.append(x)

    # воссоздаем слово из алфавитных индексов его букв учитывая регистр
    plaintext = "".join(
        upper_chars[int(element)] if isinstance(element, str) else lower_chars[element] for element in enc_letters_list
    )

    return plaintext


def full_and_even_key(word, key):
    """
    This function is creating a new keyword from original keyword.
    New keyword has the same length as a word for encryption.
    F.e. we have CONSTITUTION (len == 12) as a plain/encrypted text
    and          USA (len == 3) as a keyword
    returns      USAUSAUSAUSA (len == 12)
    """
    # fill keys to fit in word len (or make it a bit bigger)
    keyword = key
    while len(keyword) < len(word):
        keyword += key

    # выравниваем списки по длине функцией zip и берем в new_keyword только значения из list(keyword)
    new_keyword = [x[1] for x in list(zip(list(word), list(keyword)))]
    for i in range(len(new_keyword)):  # выравниваем регистр букв по регистру plaintext/cipher слова
        if word[i].isupper():
            new_keyword[i] = new_keyword[i].upper()
        if word[i].islower():
            new_keyword[i] = new_keyword[i].lower()

    return "".join(new_keyword)  # итоговое ключ-слово длина и регистр символов которого приведены к изначальному


if __name__ == "__main__":
    # set up for program
    mode = input("Select mode: encrypt/decrypt (e/d) ")
    message = input("Put text here: ")
    keyword = input("Put keyword (one word) here: ")

    # algorithm
    words = message.split()

    if mode in ("e", "encrypt"):
        print(" ".join(encrypt_vigenere(word, keyword) for word in words))
    else:
        print(" ".join(decrypt_vigenere(word, keyword) for word in words))
