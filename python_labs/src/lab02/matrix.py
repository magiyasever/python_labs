def check_matrix(mat: list[list[float | int]]) -> None:
    '''Args:
        mat: Матрица

    Returns:
        None: ничего не возвращает, только проверяет

    Raises:
        ValueError: Матрица рваная'''

    if len(mat) == 0:
        return
    etalon = len(mat[0])
    for row in mat:
        if len(row) != etalon:
            raise ValueError("Матрица рваная")

def transpose(mat: list[list[float | int]]) -> list[list]:

    '''Меняет строки и столбцы местами

    Args:
        mat: Матрица

    Returns:
        res: Транспонированная матрица

    Raises:
        ValueError: Матрица рваная'''
     
    check_matrix(mat)
    if not mat:
        return []
    res = []
    for j in range(len(mat[0])):
        new_row = []
        for row in mat:
            new_row.append(row[j])
        res.append(new_row)
    return res


def row_sums(mat: list[list[float | int]]) -> list[float]:
    '''Сумма по каждой строке

    Args: 
        mat: Матрица

    Returns:
        Список сумм по строке

    Raises:
        ValueError: строки разной длины
        ValueError: матрица пустая
    '''
    check_matrix(mat)
    if not mat:
        raise ValueError("Матрица пустая")
    res = []
    for i in range(len(mat)):
        res.append(sum(mat[i]))
    return res


def col_sums(mat: list[list[float | int]]) -> list[float]:
    '''Сумма по каждому столбцу

    Args:
        mat: Матрица

    Returns:
        Список сумм по столбцам

    Raises:
        ValueError: Строки разной длины
        ValueError: матрица пустая
    '''
    check_matrix(mat)
    if not mat:
        raise ValueError("Матрица пустая")
    res = []
    for j in range(len(mat[0])):
        k = 0
        for row in mat:
            k += row[j]
        res.append(k)
    return res


print(f'''
transpose

[[1, 2, 3]] -> {transpose([[1, 2, 3]])}
[[1], [2], [3]] -> {transpose([[1], [2], [3]])}
[[1, 2], [3, 4]] -> {transpose([[1, 2], [3, 4]])}
[] -> {transpose([])}
''')

# ValueError
# print(f'[[1, 2], [3]] -> {transpose([[1, 2], [3]])}')


print(f'''
row_sums

[[1, 2, 3], [4, 5, 6]] -> {row_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] -> {row_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] -> {row_sums([[0, 0], [0, 0]])}
''')

# ValueError
# print(f'[[1, 2], [3]] -> {row_sums([[1, 2], [3]])}')


print(f'''
col_sums

[[1, 2, 3], [4, 5, 6]] → {col_sums([[1, 2, 3], [4, 5, 6]])}
[[-1, 1], [10, -10]] → {col_sums([[-1, 1], [10, -10]])}
[[0, 0], [0, 0]] → {col_sums([[0, 0], [0, 0]])}
''')

# ValueError
# print(f'[[1, 2], [3]] -> {col_sums([[1, 2], [3]])}')