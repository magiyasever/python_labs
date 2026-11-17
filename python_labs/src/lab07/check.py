"""ЛР7. Проверка своих алгоритмов против эталона на случайных данных.

Запуск из корня репозитория: python -m src.lab07.check
"""
import random
from collections.abc import Callable

from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort, merge_sort, counting_sort
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast


def check_sorting(fn: Callable[[list[int]], list[int]], trials: int = 100) -> None:
    """Проверка сортировки против sorted на случайных списках.

    Списки длиной от 0 до 50, значения от -100 до 100, с повторами.
    Проверяется, что результат совпадает с sorted и что исходный
    список не изменился.

    Args:
        fn: Функция сортировки: принимает список, возвращает новый отсортированный.
        trials: Количество случайных списков. По умолчанию 100.

    Returns:
        None

    Raises:
        AssertionError: '{fn.__name__} ошибся на {data}: {result}'
            Результат не совпал с sorted(data).
        AssertionError: '{fn.__name__} изменила исходный список'
            Функция изменила переданный список.

    Prints:
        {fn.__name__} OK: {trials}
    """

    for _ in range(trials):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        original = list(data)
        result = fn(data)
        assert result == sorted(
            data), f'{fn.__name__} ошибся на {data}: {result}'
        assert data == original, f"{fn.__name__} изменила исходный список"

    print(f"{fn.__name__} OK: {trials}")


def check_search(trials: int = 100) -> None:
    """Проверка linear_search и binary_search против list.index.

    На каждом прогоне берётся случайный список и случайное число.
    Если число есть в списке (list.index не бросил ValueError), оба поиска
    должны его найти; дополнительно проверяются первый и последний
    элементы и заведомо отсутствующее значение. Если числа нет, оба
    поиска должны вернуть -1. binary_search проверяется на sorted(data).

    Args:
        trials: Количество проверок. По умолчанию 100.

    Returns:
        None

    Raises:
        AssertionError: 'linear_search не нашел...' / 'binary_search не нашел...'
            Поиск вернул неверный индекс или не нашёл существующий элемент.
        AssertionError: '... нашел несуществующий элемент' / '... нашел элемент, которого нет'
            Поиск нашёл элемент, которого нет в списке.

    Prints:
        OK: {trials} проверок

    Complexity:
        O(trials · m log m), m ≤ 50: в каждом прогоне sorted и линейные поиски.
    """
    for _ in range(trials):
        n = random.randint(0, 50)
        data = [random.randint(-100, 100) for _ in range(n)]
        random_number = random.randint(-100, 100)

        try:
            data.index(random_number)

            assert data[linear_search(
                data, random_number)] == random_number, "linear_search не нашел существующий случайный элемент"
            assert data[linear_search(
                data, data[0])] == data[0], "linear_search не нашел первый элемент"
            assert data[linear_search(
                data, data[-1])] == data[-1], "linear_search не нашел последний элемент"
            assert linear_search(data, 123456789) == - \
                1, "linear_search нашел несуществующий элемент"

            sort_data = sorted(data)

            assert sort_data[binary_search(
                sort_data, random_number)] == random_number, "binary_search не нашел существующий случайный элемент"
            assert sort_data[binary_search(
                sort_data, data[0])] == data[0], "binary_search не нашел первый элемент исходного списка"
            assert sort_data[binary_search(
                sort_data, data[-1])] == data[-1], "binary_search не нашел последний элемент исходного списка"
            assert binary_search(sort_data, 123456789) == - \
                1, "binary_search нашел несуществующий элемент"

        except ValueError:
            assert linear_search(data, random_number) == - \
                1, "linear_search нашел элемент, которого нет"

            sort_data = sorted(data)
            assert binary_search(sort_data, random_number) == - \
                1, "binary_search нашел элемент, которого нет"

    print(f"OK: {trials} проверок")


def check_two_sum(trials: int = 100) -> None:
    """Проверка two_sum_brute и two_sum_fast друг против друга.

    На случайных списках без повторов оба способа должны либо
    оба вернуть None, либо оба вернуть пару индексов с нужной суммой.

    Args:
        trials: Количество проверок. По умолчанию 100.

    Returns:
        None

    Raises:
        AssertionError: 'brute_find не нашел, а fast_find нашел...' (или наоборот)
            Результаты разошлись: один способ нашёл пару, а другой нет.
        AssertionError: '... вернул неверную сумму!'
            Сумма элементов по найденным индексам не равна искомому числу.

    Prints:
        OK: {trials} проверок

    Complexity:
        O(trials · m²), m ≤ 50: из-за two_sum_brute.
    """
    for _ in range(trials):
        n = random.randint(0, 50)
        data = list(set([random.randint(-100, 100) for _ in range(n)]))
        random_number = random.randint(-100, 100)

        brute_find = two_sum_brute(data, random_number)
        fast_find = two_sum_fast(data, random_number)

        if brute_find is None:
            assert fast_find is None, f"brute_find не нашел, а fast_find нашел: {fast_find}"
        else:
            assert fast_find is not None, "brute_find нашел, а fast_find - нет"

            i, j = brute_find
            assert data[i] + \
                data[j] == random_number, "brute_find вернул неверную сумму!"

            i, j = fast_find
            assert data[i] + \
                data[j] == random_number, "fast_find вернул неверную сумму!"

    print(f"OK: {trials} проверок")


def check_counting_sort(trials: int = 100) -> None:
    """★ Проверка counting_sort против sorted.

    Списки длиной от 0 до 50, значения в диапазоне [-50, 50].

    Args:
        trials: Количество проверок. По умолчанию 100.

    Returns:
        None

    Raises:
        AssertionError: 'counting_sort ошибся на {data}: {result}'
            Результат не совпал с sorted(data).
        AssertionError: 'counting_sort изменила исходный список'
            Функция изменила переданный список.

    Prints:
        counting_sort OK: {trials}

    Complexity:
        O(trials · (m log m + k)), m ≤ 50, k = 101 (размер диапазона).
    """
    for _ in range(trials):
        n = random.randint(0, 50)
        lo, hi = -50, 50
        data = [random.randint(lo, hi) for _ in range(n)]
        original = list(data)

        result = counting_sort(data, lo, hi)

        assert result == sorted(
            data), f'counting_sort ошибся на {data}: {result}'
        assert data == original, "counting_sort изменила исходный список"

    print(f"counting_sort OK: {trials}")


if __name__ == "__main__":
    print()
    print("Проверка сортировок")
    print()
    check_sorting(bubble_sort)
    check_sorting(insertion_sort)
    check_sorting(selection_sort)
    check_sorting(merge_sort)
    check_counting_sort()
    print("Сортировки в порядке")
    print()

    print("-------------------------")
    print("Проверка поиска")
    print()
    check_search()
    print("Поиск в порядке")
    print()

    print("-------------------------")
    print("Проверка поиска суммы")
    print()
    check_two_sum()
    print("Поиск суммы в порядке")
    print()
    print("-------------------------")

    print("ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
