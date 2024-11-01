import string


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    # create alphabet of both upper and lower case letters
    lower_chars = dict(enumerate([char for char in string.ascii_lowercase]))
    inverted_lower_chars = {v: k for k, v in lower_chars.items()}
    upper_chars = dict(enumerate([char for char in string.ascii_uppercase]))
    inverted_upper_chars = {v: k for k, v in upper_chars.items()}

    list_of_numbers = []

    for char in plaintext:  # getting alphabetical number of every char in word
        if char.isupper() and not (char.isnumeric() or char in string.punctuation):
            list_of_numbers.append(inverted_upper_chars[char])
        elif char.islower() and not (char.isnumeric() or char in string.punctuation):
            list_of_numbers.append(inverted_lower_chars[char])
        else:
            list_of_numbers.append(char)

    nw = []
    for i in range(len(list_of_numbers)):
        if type(list_of_numbers[i]) is int:
            list_of_numbers[i] += shift  # shifting numbers [only if it is not a specific symbol!!!!]
            if list_of_numbers[i] > 25:
                list_of_numbers[i] -= 26  # reducing number to stay inside alphabet length

        if plaintext[i].isupper() and not (plaintext[i].isnumeric() or plaintext[i] in string.punctuation):
            nw.append(upper_chars[list_of_numbers[i]])
        elif plaintext[i].islower() and not (plaintext[i].isnumeric() or plaintext[i] in string.punctuation):
            nw.append(lower_chars[list_of_numbers[i]])
        else:
            nw.append(plaintext[i])

        # last operation breakdown: 1) it creates a new list of encoded word chars
        #                           2) operator "if" checks was character in upper case or lower case
        #                           3) correspondingly to p2 it appends the correct new character
        #                           to the end of a string
    ciphertext = ''.join(nw)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    # create alphabet of both upper and lower case letters
    lower_chars = dict(enumerate([char for char in string.ascii_lowercase]))
    inverted_lower_chars = {v: k for k, v in lower_chars.items()}
    upper_chars = dict(enumerate([char for char in string.ascii_uppercase]))
    inverted_upper_chars = {v: k for k, v in upper_chars.items()}

    list_of_numbers = []

    for char in ciphertext:  # getting alphabetical number of every char in word
        if char.isupper() and not (char.isnumeric() or char in string.punctuation):
            list_of_numbers.append(inverted_upper_chars[char])
        elif char.islower() and not (char.isnumeric() or char in string.punctuation):
            list_of_numbers.append(inverted_lower_chars[char])
        else:
            list_of_numbers.append(char)

    nw = []
    for i in range(len(list_of_numbers)):
        if type(list_of_numbers[i]) is int:
            list_of_numbers[i] -= shift  # shifting numbers [only if it is not a specific symbol!!!!]
            if list_of_numbers[i] < 0:
                list_of_numbers[i] += 26  # reducing number to stay inside alphabet length

        if ciphertext[i].isupper() and not (ciphertext[i].isnumeric() or ciphertext[i] in string.punctuation):
            nw.append(upper_chars[list_of_numbers[i]])
        elif ciphertext[i].islower() and not (ciphertext[i].isnumeric() or ciphertext[i] in string.punctuation):
            nw.append(lower_chars[list_of_numbers[i]])
        else:
            nw.append(ciphertext[i])

        # last operation breakdown: 1) it creates a new list of encoded word chars
        #                           2) operator "if" checks was character in upper case or lower case
        #                           3) correspondingly to p2 it appends the correct new character
        #                           to the end of a string
    plaintext = ''.join(nw)

    return plaintext


if __name__ == "__main__":
    # set up for program
    mode = input("Select mode: encrypt/decrypt (e/d) ")
    message = input("Put text here: ")
    shift = int(input("Put shifting value: "))

    # algorithm
    words = message.split()
    print(' '.join(
        [encrypt_caesar(word, shift) if mode == 'e' or mode == 'encrypt' else decrypt_caesar(word, shift) for word in
         words])
    )
