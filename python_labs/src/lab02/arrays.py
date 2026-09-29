def mmax(s):
    """Возвращает наибольший элемент последовательности.

    Аналог встроенной функции ``max`` для одного итерируемого аргумента.

    Args:
        s: Непустой итерируемый объект с числами, которые можно сравнивать.

    Returns:
        Наибольшее значение из ``s``."""
    res = s[0]
    for x in s:
        if x > res:
            res = x
    return res
def mmin(s):
    """Возвращает наименьший элемент последовательности.

    Аналог встроенной функции ``min`` для одного итерируемого аргумента.

    Args:
        s: Непустой итерируемый объект с числами, которые можно сравнивать.

    Returns:
        Наименьшее значение из ``s``."""
    res = s[0]
    for x in s:
            if x < res:
                res = x
    return res


def min_max(nums: list[float | int])  -> tuple[float | int, float | int]:
    """Вычисляет максимум и минимум списка

    Args:

        a: Список чисел (целых и вещественных)

    Returns:

        Кортеж (минимум, максимум)

    Raises:

        ValueError: если список пустой

    """
    if len(nums) == 0:
        raise ValueError
    newl = (mmin(nums), mmax(nums))
    return newl



def unique_sorted(nums: list[float | int]) -> list[float | int]:
    n = list(set(nums))
    """Возвращает отсортированный список

    Args:

        a: Список чисел (целых и вещественных)

    Returns:

        Отсортированный список уникальных элементов

    """
    for i in range(len(n)):
        for k in range(len(n) - 1):
            if n[k] > n[k + 1]:
                n[k], n[k + 1] = n[k + 1], n[k]
    return n

def flatten(mat: list[list | tuple]) -> list:
    """Переводит матрицу в вектор

    Args:

        a: Список в котором содержатся списки или кортежи

    Returns:

        result: Список

    Raises:

        TypeError: Если элемент не является списком или кортежем

    """
    result = []
    for x in mat:
        if not isinstance(x, (tuple, list)):
            raise TypeError
        result.extend(x)
    return result


print(f'''
min_max

[3, -1, 5, 5, 0] -> {min_max([3, -1, 5, 5, 0])}
[42] -> {min_max([42])}
[-5, -2, -9] -> {min_max([-5, -2, -9])}
[1.5, 2, 2.0, -3.1] -> {min_max([1.5, 2, 2.0, -3.1])}
''')
# выводит ValueError
#print(f'[] -> {min_max([])}')

print(f'''
unique_sorted

[3, 1, 2, 1, 3] -> {unique_sorted([3, 1, 2, 1, 3])}
[] -> {unique_sorted([])}
[-1, -1, 0, 2, 2] -> {unique_sorted([-1, -1, 0, 2, 2])}
[1.0, 1, 2.5, 2.5, 0] -> {unique_sorted([1.0, 1, 2.5, 2.5, 0])}
''')

print(f'''
flatten

[[1, 2], [3, 4]] -> {flatten([[1, 2], [3, 4]])}
[[1, 2], (3, 4, 5)] -> {flatten([[1, 2], (3, 4, 5)])}
[[1], [], [2, 3]] -> {flatten([[1], [], [2, 3]])}
''')

# выводит TypeError
print(f'[[1, 2], "ab"] -> {flatten([[1, 2], "ab"])}') 
    
