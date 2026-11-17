"""ЛР7 График времени работы сортировок по данным data/lab07/bench.csv.

Запуск из корня репозитория: python -m src.lab07.plot
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def create_plot() -> None:
    """График зависимости времени сортировок от n.

    Читает data/lab07/bench.csv, берёт строки с task == "sort",
    превращает значения вида "> 60" в число 60 и строит по одной
    линии на каждую сортировку. Обе оси логарифмические: так
    O(n²) и O(n log n) видны как прямые с разным наклоном.

    Args:
        None

    Returns:
        None

    Side effects:
        Сохраняет график в images/lab07/sorting_graph.png
        и показывает его в окне (plt.show).

    Prints:
        График сохранен в images/lab07/sorting_graph.png
    """
    df = pd.read_csv("data/lab07/bench.csv")

    df_sort = df[df["task"] == "sort"].copy()

    df_sort["seconds"] = df_sort["seconds"].astype(
        str).str.replace(r'>\s*', '', regex=True).astype(float)

    pivot_df = df_sort.pivot(index="n", columns="impl", values="seconds")

    ax = pivot_df.plot(
        marker='o',
        logx=True,
        logy=True,
        figsize=(10, 6),
        title="Сравнение времени работы сортировок",
        linewidth=2
    )

    ax.set_xlabel("Размер списка (n)")
    ax.set_ylabel("Время (секунды)")
    ax.grid(True, which="both", ls="--", alpha=0.5)

    Path("images/lab07").mkdir(parents=True, exist_ok=True)
    plt.savefig("images/lab07/sorting_graph.png", bbox_inches="tight")
    print("График сохранен в images/lab07/sorting_graph.png")

    plt.show()


if __name__ == "__main__":
    create_plot()
