"""ЛР7. Бенчмарк: свои алгоритмы против встроенных.

Запуск из корня репозитория: python -m src.lab07.bench
"""
import random
import timeit
from collections.abc import Callable
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import (bubble_sort, counting_sort, insertion_sort,merge_sort, selection_sort)

QUADRATIC_LIMIT = 10_000  # квадратичные сортировки на n больше этого не запускаем

Row = tuple[str, int, str, float | str]  # (task, n, impl, seconds); seconds может быть "> 60"

def measure(fn: Callable[[], object], number: int = 1, repeat: int = 3) -> float:
    """Время одного запуска fn в секундах.

    Делается repeat замеров, в каждом fn запускается number раз подряд.
    Берётся лучший замер (меньше всего помех от системы) и делится на number.

    Args:
        fn: Функция без аргументов, обычно lambda с вызовом алгоритма.
        number: Сколько раз запускать fn в одном замере. По умолчанию 1.
        repeat: Сколько замеров сделать. По умолчанию 3.

    Returns:
        Время одного запуска fn в секундах.
    """
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


def bench_sorts(n: int) -> list[Row]:
    """Замер sorted, merge_sort и трёх квадратичных сортировок на одних данных.

    Квадратичные сортировки при n > QUADRATIC_LIMIT не запускаются:
    это около 10¹⁰ шагов, вместо времени в таблицу пишется "> 60".

    Args:
        n: Размер случайного списка.

    Returns:
        Строки таблицы вида ("sort", n, имя функции, секунды).
    """
    data = [random.randint(-10_000, 10_000) for _ in range(n)]  # одни данные на всех
    rows = []

    # быстрые: много запусков, иначе на n=1000 время ~0.0001 с тонет в шуме
    rows.append(("sort", n, "sorted", measure(lambda: sorted(data), number=100, repeat=5)))
    rows.append(("sort", n, "merge_sort", measure(lambda: merge_sort(data), repeat=3)))

    # квадратичные: один и тот же код для всех трёх — через цикл
    for fn in (bubble_sort, insertion_sort, selection_sort):
        if n > QUADRATIC_LIMIT:
            rows.append(("sort", n, fn.__name__, "> 60"))           # ~10¹⁰ шагов
        else:
            rep = 3 if n <= 1_000 else 1                              # на 10⁴ один прогон — секунды
            rows.append(("sort", n, fn.__name__, measure(lambda: fn(data), repeat=rep)))
    return rows


def bench_counting(n: int = 1_000_000) -> list[Row]:
    """★ Целые в узком диапазоне: counting_sort обгоняет sorted.

    Значения от 0 до 100, поэтому k = 101 намного меньше n,
    и O(n + k) выигрывает у O(n log n).

    Args:
        n: Размер случайного списка. По умолчанию 1 000 000.

    Returns:
        Две строки таблицы: ("count", n, "sorted" / "counting_sort", секунды).
    """
    lo, hi = 0, 100
    data = [random.randint(lo, hi) for _ in range(n)]
    return [
        ("count", n, "sorted", measure(lambda: sorted(data), number=5)),
        ("count", n, "counting_sort", measure(lambda: counting_sort(data, lo, hi), number=5)),
    ]


def bench_search(n: int = 100_000, q: int = 10_000) -> list[Row]:
    """Линейный поиск против бинарного: q запросов к списку из n чисел.

    Время сортировки для бинарного поиска замеряется отдельной строкой
    и добавляется в строку "sort + binary": это его честная полная цена.

    Args:
        n: Размер списка. По умолчанию 100 000.
        q: Количество поисковых запросов. По умолчанию 10 000.

    Returns:
        Четыре строки таблицы: linear, sort_only, binary и sort + binary.
    """
    # диапазон в 10 раз шире n: большинство запросов НЕ найдётся → худший случай для linear
    data = [random.randint(0, 10 * n) for _ in range(n)]
    queries = [random.randint(0, 10 * n) for _ in range(q)]
    sorted_data = sorted(data)

    def linear_runner() -> None:
        """Все q запросов линейным поиском по data."""
        for x in queries:
            linear_search(data, x)

    def binary_runner() -> None:
        """Все q запросов бинарным поиском по sorted_data."""
        for x in queries:
            binary_search(sorted_data, x)

    t_linear = measure(linear_runner, repeat=1)                 # ~20 с, повторять дорого
    t_sort = measure(lambda: sorted(data), repeat=5)
    t_binary = measure(binary_runner, number=10, repeat=3)
    return [
        ("search", n, f"linear x{q}", t_linear),
        ("search", n, "sort_only", t_sort),
        ("search", n, f"binary x{q}", t_binary),
        ("search", n, "sort + binary", t_sort + t_binary),   # честная полная цена бинарного
    ]


def bench_two_sum(n: int) -> list[Row]:
    """two_sum_brute против two_sum_fast в худшем случае.

    Подходящая пара — только два последних элемента, поэтому
    перебор проверяет все пары, а словарь проходит весь список.

    Args:
        n: Размер списка (n ≥ 2).

    Returns:
        Две строки таблицы: ("two_sum", n, имя функции, секунды).
    """
    # все числа в 0..10⁶, а в конце два огромных: target даёт ТОЛЬКО последняя пара
    # → перебор проверяет все пары, это худший случай O(n²)
    data = random.sample(range(0, 10**6), n - 2) + [10**7, 10**7 + 1]
    target = 2 * 10**7 + 1
    return [
        ("two_sum", n, "two_sum_brute", measure(lambda: two_sum_brute(data, target), repeat=1)),
        ("two_sum", n, "two_sum_fast", measure(lambda: two_sum_fast(data, target), number=100)),
    ]


def print_table(rows: list[Row]) -> None:
    """Печать результатов таблицей с выравниванием по столбцам.

    Args:
        rows: Строки (task, n, impl, seconds). Если seconds не float
            (например "> 60"), печатается как есть.

    Returns:
        None
    """
    print(f"{'task':<8} | {'n':>8} | {'impl':<15} | {'seconds':>10}")
    print("-" * 52)
    for task, n, impl, sec in rows:
        sec_str = f"{sec:10.6f}" if isinstance(sec, float) else f"{sec:>10}"
        print(f"{task:<8} | {n:>8} | {impl:<15} | {sec_str}")


if __name__ == "__main__":
    random.seed(42)
    all_rows = []

    print("Бенчмарк сортировки")
    for n in (1_000, 10_000, 100_000):
        all_rows += bench_sorts(n)

    print("Бенчмарк Counting Sort")
    all_rows += bench_counting()

    print("Бенчмарк поисков")
    all_rows += bench_search()

    print("Бенчмарк Two Sum")
    for n in (1_000, 10_000):
        all_rows += bench_two_sum(n)

    all_rows = [(t, n, i, round(s, 6) if isinstance(s, float) else s)
                for t, n, i, s in all_rows]

    print("\nРезультаты:\n")
    print_table(all_rows)

    Path("data/lab07").mkdir(parents=True, exist_ok=True)
    write_csv(all_rows, "data/lab07/bench.csv", header=("task", "n", "impl", "seconds"))
    print("\nРезультаты сохранены в data/lab07/bench.csv")
