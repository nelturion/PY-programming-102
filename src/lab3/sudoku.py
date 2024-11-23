import multiprocessing
import pathlib
import random
import threading
import time
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    res = []
    for i in range(0, len(values), n):
        res.append(values[i:i + n])
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    >>> get_row([['1', '2', '.'],['4', '5', '6'],['7', '8', '9']], (0, 3))
    ['1', '2', '.']
    """
    """                 [1, 2, .]
     У нас есть поле:   [4, 5, 6]
                        [7, 8, 9]
    функция должна вернуть строку (row), на которую указывает координата pos(row, col) 
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for row in grid:
        col.append(row[pos[1]])
    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    top_left_pos = (pos[0] - (pos[0] % 3), pos[1] - (pos[1] % 3))
    block_rows = [top_left_pos[0], top_left_pos[0] + 1, top_left_pos[0] + 2]
    block_cols = [top_left_pos[1], top_left_pos[1] + 1, top_left_pos[1] + 2]
    block_vals = []
    for i in range(3):
        for j in range(3):
            block_vals.append(grid[block_rows[i]][block_cols[j]])
    return block_vals


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
    (-1, -1)
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ".":
                return i, j
    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    possible_values = set([str(i) for i in range(1, 10)]).union(".")
    possible_values = possible_values.difference(set(get_row(grid, pos)))
    possible_values = possible_values.difference(set(get_col(grid, pos)))
    possible_values = possible_values.difference(set(get_block(grid, pos)))
    return possible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]] | bool:
    """ Решение пазла, заданного в grid
        Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    new_grid = grid
    if check_solution(new_grid):
        return new_grid
    else:
        empty = find_empty_positions(new_grid)
        possible = sorted(list(find_possible_values(new_grid, empty)))
        for variant in possible:
            new_grid[empty[0]][empty[1]] = variant
            solve(new_grid)
            if check_solution(new_grid):
                return new_grid
            new_grid[empty[0]][empty[1]] = '.'
        return False


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> solution = [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    >>> check_solution(solution)
    True
    >>> solution = [['5', '2', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    >>> check_solution(solution)
    False
    """
    # Проверяем количество различных цифр и наличие пустых ячеек
    if find_empty_positions(solution) == (-1, -1):
        for i in range(len(solution)):
            column_set = set(get_col(solution, (i, i)))
            if len(column_set) < 9:
                return False  # колонка неправильная

            row_set = set(get_row(solution, (i, i)))
            if len(row_set) < 9:
                return False  # строка неправильная

        for i in range(0, len(solution), 3):
            for j in range(0, len(solution[0]), 3):
                block_set = set(get_block(solution, (i, j)))
                if len(block_set) < 9:
                    return False  # блок неправильный

        return True  # Нигде не возникло ошибок, так что все ок
    else:
        return False  # где-то нашли '.'


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    def transposing(grid: list[list[str]]) -> list[list[str]]:
        """ Transposing the whole grid """
        grid = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
        return grid

    def swap_rows_small(grid: list[list[str]]) -> list[list[str]]:
        """ Swap the two rows """
        # получение случайного района и случайной строки
        n = 3
        area = random.randrange(0, n, 1)  # area - это 3 блока
        line1 = random.randrange(0, n, 1)

        N1 = area * n + line1  # номер 1 строки для обмена

        line2 = random.randrange(0, n, 1)
        while line1 == line2:
            line2 = random.randrange(0, n, 1)

        N2 = area * n + line2  # номер 2 строки для обмена

        grid[N1], grid[N2] = grid[N2], grid[N1]
        return grid

    def swap_cols_small(grid: list[list[str]]) -> list[list[str]]:
        grid = transposing(grid)
        grid = swap_rows_small(grid)
        grid = transposing(grid)
        return grid

    def swap_rows_area(grid: list[list[str]]) -> list[list[str]]:
        area1 = random.randint(0, 2)  # индекс областей, которые хотим поменять местами
        area2 = random.randint(0, 2)
        while area2 == area1:
            area2 = random.randint(0, 2)

        for i in range(0, 3):
            N1, N2 = area1 * 3 + i, area2 * 3 + i  # построчно меняем местами области
            grid[N1], grid[N2] = grid[N2], grid[N1]
        return grid

    def swap_cols_area(grid: list[list[str]]) -> list[list[str]]:
        grid = transposing(grid)
        grid = swap_rows_area(grid)
        grid = transposing(grid)
        return grid

    def shuffle(grid: list[list[str]], swaps=10) -> list[list[str]]:
        shuffle_functions = [transposing,
                             swap_rows_area,
                             swap_cols_area,
                             swap_cols_small,
                             swap_rows_small]
        for i in range(swaps):
            id_func = random.choice(shuffle_functions)
            grid = id_func(grid)
        return grid

    def dot(grid: list[list[str]], N: int) -> list[list[str]]:
        for i in range(81 - N):
            pos = (random.randint(0, 8), random.randint(0, 8))
            while grid[pos[0]][pos[1]] == '.':
                pos = (random.randint(0, 8), random.randint(0, 8))
            grid[pos[0]][pos[1]] = '.'
        return grid

    n = 3
    grid = [[((i * n + i // n + j) % (n * n) + 1) for j in range(n * n)] for i in range(n * n)]
    grid = shuffle(grid)
    grid = dot(grid, N)
    return grid


def run_solve(filename: str):
    """
    Sudoku solver with timer. Used for multithread solution
    """
    grid = read_sudoku(filename)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f"{filename}: {end - start}\n")


if __name__ == "__main__":
    grid = read_sudoku("unsolvable_generated.txt")
    display(grid)
    sol = solve(grid)
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        p = multiprocessing.Process(target=run_solve, args=(filename,))
        p.start()
    time.sleep(10)
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        t = threading.Thread(target=run_solve, args=(filename,))
        t.start()

'''
if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        start = time.time()
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
        end = time.time()
        print("solving time: ", end-start)
'''
