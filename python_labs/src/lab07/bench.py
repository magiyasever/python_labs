"""ЛР7. Бенчмарк: свои алгоритмы против встроенных.

Запуск из корня репозитория: python -m src.lab07.bench
"""
import random
import timeit
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import (bubble_sort, counting_sort, insertion_sort,
                               merge_sort, selection_sort)

QUADRATIC_LIMIT = 10_000  # квадратичные сортировки на n больше этого не запускаем


def measure(fn, number=1, repeat=3) -> float:
    """Время ОДНОГО запуска fn: number запусков подряд, repeat таких замеров,
    берём лучший замер и делим на number."""
    return min(timeit.repeat(fn, number=number, repeat=repeat)) / number


def bench_sorts(n: int) -> list[tuple]:
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


def bench_counting(n: int = 1_000_000) -> list[tuple]:
    """★ Целые в узком диапазоне: counting_sort обгоняет sorted."""
    lo, hi = 0, 100
    data = [random.randint(lo, hi) for _ in range(n)]
    return [
        ("count", n, "sorted", measure(lambda: sorted(data), number=5)),
        ("count", n, "counting_sort", measure(lambda: counting_sort(data, lo, hi), number=5)),
    ]


def bench_search(n: int = 100_000, q: int = 10_000) -> list[tuple]:
    # диапазон в 10 раз шире n: большинство запросов НЕ найдётся → худший случай для linear
    data = [random.randint(0, 10 * n) for _ in range(n)]
    queries = [random.randint(0, 10 * n) for _ in range(q)]
    sorted_data = sorted(data)

    def linear_runner():
        for x in queries:
            linear_search(data, x)

    def binary_runner():
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


def bench_two_sum(n: int) -> list[tuple]:
    # все числа в 0..10⁶, а в конце два огромных: target даёт ТОЛЬКО последняя пара
    # → перебор проверяет все пары, это худший случай O(n²)
    data = random.sample(range(0, 10**6), n - 2) + [10**7, 10**7 + 1]
    target = 2 * 10**7 + 1
    return [
        ("two_sum", n, "two_sum_brute", measure(lambda: two_sum_brute(data, target), repeat=1)),
        ("two_sum", n, "two_sum_fast", measure(lambda: two_sum_fast(data, target), number=100)),
    ]


def print_table(rows: list[tuple]) -> None:
    print(f"{'task':<8} | {'n':>8} | {'impl':<15} | {'seconds':>10}")
    print("-" * 52)
    for task, n, impl, sec in rows:
        sec_str = f"{sec:10.6f}" if isinstance(sec, float) else f"{sec:>10}"
        print(f"{task:<8} | {n:>8} | {impl:<15} | {sec_str}")


if __name__ == "__main__":
    random.seed(42)
    all_rows = []

    print("Бенчмаркаю сортировки...")
    for n in (1_000, 10_000, 100_000):
        all_rows += bench_sorts(n)

    print("Бенчмаркаю Counting Sort...")
    all_rows += bench_counting()

    print("Бенчмаркаю поиски...")
    all_rows += bench_search()

    print("Бенчмаркаю Two Sum...")
    for n in (1_000, 10_000):
        all_rows += bench_two_sum(n)

    all_rows = [(t, n, i, round(s, 6) if isinstance(s, float) else s)
                for t, n, i, s in all_rows]

    print("\nРезультаты:\n")
    print_table(all_rows)

    Path("data/lab07").mkdir(parents=True, exist_ok=True)
    write_csv(all_rows, "data/lab07/bench.csv", header=("task", "n", "impl", "seconds"))
    print("\nРезультаты сохранены в data/lab07/bench.csv")