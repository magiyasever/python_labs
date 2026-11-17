"""ЛР7. Сортировки. Каждая возвращает новый список и не меняет исходный."""


def bubble_sort(nums: list[int]) -> list[int]:
    """Сортировка пузырьком.

    Проходим по списку и меняем местами соседей, стоящих не по порядку;
    за проход максимум «всплывает» в конец. Если за проход не было ни
    одного обмена, список уже отсортирован и выходим досрочно.

    Args:
        nums: Список чисел. Не изменяется.

    Returns:
        Новый список, отсортированный по возрастанию.

    Complexity:
        Время: O(n²) в среднем и худшем случае,
            O(n) на уже отсортированных данных (флаг swapped).
        Память: O(n) на копию списка.

    Examples:
        bubble_sort([3, 1, 2]) -> [1, 2, 3]
        bubble_sort([2, 2, 1]) -> [1, 2, 2]
        bubble_sort([]) -> []
    """
    a = list(nums)                       # копия, исходный список не трогаем
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        if not swapped:                  # проход без обменов: уже отсортировано
            break
    return a



def insertion_sort(nums: list[int]) -> list[int]:
    """Сортировка вставками.

    Левая часть списка всегда отсортирована. Берём очередной элемент
    и сдвигаем его влево, пока он не встанет на своё место.

    Args:
        nums: Список чисел. Не изменяется.

    Returns:
        Новый список, отсортированный по возрастанию.

    Complexity:
        Время: O(n²) в среднем и худшем случае,
            O(n) на почти отсортированных данных.
        Память: O(n) на копию списка.

    Examples:
        insertion_sort([4, 2, 3, 1]) -> [1, 2, 3, 4]
        insertion_sort([2, 2, 1]) -> [1, 2, 2]
        insertion_sort([]) -> []
    """
    a = list(nums)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def selection_sort(nums: list[int]) -> list[int]:
    """Сортировка выбором.

    На каждом шаге находим минимум в неотсортированной части
    и меняем его местами с первым элементом этой части.

    Args:
        nums: Список чисел. Не изменяется.

    Returns:
        Новый список, отсортированный по возрастанию.

    Complexity:
        Время: O(n²) всегда, даже на отсортированных данных;
            обменов при этом всего O(n).
        Память: O(n) на копию списка.

    Examples:
        selection_sort([3, 1, 2]) -> [1, 2, 3]
        selection_sort([2, 2, 1]) -> [1, 2, 2]
        selection_sort([]) -> []
    """
    a = list(nums)
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a

def merge_sort(nums: list[int]) -> list[int]:
    """Сортировка слиянием снизу вверх (без рекурсии).

    Сливаем соседние отсортированные отрезки длины 1, 2, 4, …,
    пока весь список не станет одним отрезком.

    Args:
        nums: Список чисел. Не изменяется.

    Returns:
        Новый список, отсортированный по возрастанию.

    Complexity:
        Время: O(n log n) всегда: log n уровней, на каждом сливаем n элементов.
        Память: O(n).

    Examples:
        merge_sort([5, 2, 4, 1]) -> [1, 2, 4, 5]
        merge_sort([]) -> []
    """
    arr = list(nums)
    n = len(arr)
    step = 1

    while step < n:
        for left in range(0, n, 2 * step):
            mid = left + step
            right = min(left + 2 * step, n)

            if mid >= n:
                continue

            merged = []
            i, j = left, mid

            while i < mid and j < right:
                if arr[i] <= arr[j]:
                    merged.append(arr[i])
                    i += 1
                else:
                    merged.append(arr[j])
                    j += 1

            while i < mid:
                merged.append(arr[i])
                i += 1
            while j < right:
                merged.append(arr[j])
                j += 1

            arr[left:right] = merged

        step *= 2

    return arr


def counting_sort(nums: list[int], lo: int, hi: int) -> list[int]:
    """★ Сортировка подсчётом для целых чисел в диапазоне [lo, hi].

    Считаем, сколько раз встречается каждое значение,
    и выписываем значения по порядку. Элементы не сравниваются.

    Args:
        nums: Список целых чисел, каждое из диапазона [lo, hi]. Не изменяется.
        lo: Минимально возможное значение.
        hi: Максимально возможное значение.

    Returns:
        Новый список, отсортированный по возрастанию.

    Raises:
        IndexError: Если в nums есть число больше hi.
            Число меньше lo даёт отрицательный индекс: неверный
            результат без ошибки или тот же IndexError.

    Complexity:
        Время: O(n + k), где k = hi - lo + 1.
        Память: O(k) на счётчики и O(n) на результат.

    Examples:
        counting_sort([3, 1, 3, 0], 0, 3) -> [0, 1, 3, 3]
        counting_sort([], 0, 10) -> []
    """
    count = [0] * (hi - lo + 1)

    for x in nums:
        count[x - lo] += 1

    res = []
    for i in range(len(count)):
        res.extend([lo + i] * count[i])

    return res
