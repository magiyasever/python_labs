def bubble_sort(nums):
    """Новый список, отсортированный по возрастанию. Исходный не меняется.
 
    bubble_sort([3, 1, 2]) -> [1, 2, 3]
    bubble_sort([2, 2, 1]) -> [1, 2, 2]
    bubble_sort([]) -> []
    """
    a = len(nums)
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                swapped = True
        if not swapped:
            break
    return a

    
 
 
def insertion_sort(nums):
    a = list(nums)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
 
 
def selection_sort(nums):
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
    '''★ Сортировка слиянием (без рекурсии)

    Args:
        nums: Список чисел

    Returns:
        arr: Отсортированный список чисел

    Complexity:
        O(n log n): Линейно-логарифмическая сложность
    '''
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
    '''★ Сортировка подсчетом для целых чисел в диапазоне [lo, hi]

    Args:
        nums: Список чисел
        lo: Минимально возможное значение
        hi: Максимально возможное значение

    Returns:
        res: Отсортированный список чисел

    Complexity:
        O(n + k): Линейная сложность, k = (hi - lo)
    '''
    count = [0] * (hi - lo + 1)

    for x in nums:
        count[x - lo] += 1

    res = []
    for i in range(len(count)):
        res.extend([lo + i] * count[i])

    return res