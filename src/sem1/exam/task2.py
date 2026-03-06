"""
Реализовать метод, принимающий на вход строковую переменную - исходный текст программы на C++, Java,
вырезающий из этой строки все комментарии и возвращающий результат в виде строки.

possible comment types:
// endline comment

/* inline comment */

/*
    multiline comment
*/

/**
* Documentation (actually it's the same as multiline comment, but with extra *)
**/
"""

def file_reader(path: str) -> list[str]:
    rr = []
    with open(path) as file:
        r = file.readlines()
        for line in r:
            rr.append(line.strip())
        return rr


def delete_endline_comment(line: str) -> str:
    """
    deletes endline comment. comment that starts with '//'
    :param line: line of code that has comment (or just ends with '//')
    :return: line of code without comment
    """
    return line.split('//')[0]


def delete_inline_comment(line: str) -> str:
    """
    deletes inline comment. comment that starts with '/*' and ends with '*/'.
    Another way to solve this - split input line at '/*'
    """
    res = ''
    comment_exists = len(line.split('/*')) - 1  # exists > 1, not exist == 1
    if comment_exists == 0:
        return line

    comment_start_index = 0
    comment_end_index = 0
    for i in range(len(line) - 1):
        if line[i] == '/' and line[i + 1] == '*':
            comment_start_index = i
            break
    for i in range(len(line) - 1):
        if line[i] == '*' and line[i + 1] == '/':
            comment_end_index = i
            break
    res = str(line[:comment_start_index] + line[comment_end_index+2:])
    return res


def delete_multiline_comment(lines: list[str]) -> list[str]:
    """
    deletes multiline comment. comment that starts with '/*' has some lines in it that are not marked and ends with '*/'
    :param lines: list of lines
    """
    res = []
    comment_started_flag = False
    comment_ended_flag = False
    for i in range(len(lines)):  # сработает, если учитывать, что комментарии написаны по стандарту!
        if lines[i] == '/*' or lines[i] == '/**':
            comment_started_flag = True
            lines[i] = ''
        if lines[i] == '*/' or lines[i] == '**/' and comment_started_flag:
            lines[i] = ''
            comment_ended_flag = True
            comment_started_flag = False

        if not comment_started_flag:
            res.append(lines[i])
    return res


def print_in_file(code: list[str]) -> None:
    with open("clear_code.txt", "w") as file:
        for line in code:
            file.write(line + '\n')


if __name__ == '__main__':
    #print(file_reader('java_code.txt'))
    code_text = file_reader('java_code.txt')
    code_text = delete_multiline_comment(code_text)

    res = []
    for line in code_text:
        res.append(delete_endline_comment(line))
    res2 = []
    for line in res:
        res2.append(delete_inline_comment(line))

    print_in_file(res2)
    #print(res2)

