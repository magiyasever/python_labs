"""ЛР7. Алгоритмы поиска: линейный, бинарный и задача Two Sum."""


def linear_search(nums: list[int], x: int) -> int:
    """Линейный поиск: индекс первого вхождения x или -1.

    Идём по списку слева направо и сравниваем каждый элемент с x.
    Порядок элементов не важен.

    Args:
        nums: Список чисел (в любом порядке).
        x: Искомое значение.

    Returns:
        Индекс первого вхождения x в nums или -1, если x нет.

    Complexity:
        Время: O(n) в худшем случае (x нет или он последний), O(1) в лучшем.
        Память: O(1).

    Examples:
        linear_search([4, 2, 7, 2], 2) -> 1
        linear_search([4, 2, 7, 2], 9) -> -1
        linear_search([], 1) -> -1
    """
    for i in range(len(nums)):
        if nums[i] == x:
            return i
    return -1



def binary_search(sorted_nums: list[int], x: int) -> int:
    """Бинарный поиск: индекс x в отсортированном по возрастанию списке или -1.

    Смотрим в середину диапазона [lo, hi]: если там x, возвращаем индекс;
    если x больше, отбрасываем левую половину, если меньше, правую.
    На неотсортированном списке результат не определён.

    Args:
        sorted_nums: Список чисел, отсортированный по возрастанию.
        x: Искомое значение.

    Returns:
        Индекс любого вхождения x в sorted_nums или -1, если x нет.

    Complexity:
        Время: O(log n), каждый шаг вдвое сокращает диапазон.
        Память: O(1).

    Examples:
        binary_search([1, 3, 5, 7], 5) -> 2
        binary_search([1, 3, 5, 7], 4) -> -1
        binary_search([5], 5) -> 0
        binary_search([], 5) -> -1
    """
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] < x:
            lo = mid + 1
        elif sorted_nums[mid] > x:
            hi = mid - 1
        else:
            return mid
    return -1


def two_sum_brute(nums: list[int], target: int) -> tuple[int, int] | None:
    """Two Sum перебором: пара индексов с суммой элементов, равной target.

    Проверяем все пары (i, j), где i < j.

    Args:
        nums: Список чисел.
        target: Искомая сумма двух элементов.

    Returns:
        Первая найденная пара индексов (i, j), i < j,
        nums[i] + nums[j] == target, или None, если такой пары нет.

    Complexity:
        Время: O(n²), всего около n²/2 пар.
        Память: O(1).

    Examples:
        two_sum_brute([2, 7, 11, 15], 9) -> (0, 1)
        two_sum_brute([1, 2], 10) -> None
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def two_sum_fast(nums: list[int], target: int) -> tuple[int, int] | None:
    """Two Sum за один проход со словарём «значение -> индекс».

    Для каждого элемента num проверяем, встречалось ли раньше
    target - num. Сначала проверка, потом запись в словарь, поэтому
    элемент не складывается сам с собой.

    Args:
        nums: Список чисел.
        target: Искомая сумма двух элементов.

    Returns:
        Пара индексов (i, j), i < j, nums[i] + nums[j] == target,
        или None, если такой пары нет. При нескольких ответах
        допустим любой.

    Complexity:
        Время: O(n), проверка `in` у словаря в среднем O(1).
        Память: O(n) на словарь.

    Examples:
        two_sum_fast([2, 7, 11, 15], 9) -> (0, 1)
        two_sum_fast([1, 2], 10) -> None
    """
    num_dict = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return (num_dict[complement], i)
        num_dict[num] = i
    return None
