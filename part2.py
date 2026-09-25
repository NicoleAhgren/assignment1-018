from part1 import lin_reg, time_once
import random
import math
import matplotlib.pyplot as plt


def random_list(n):
    lst = []
    for _ in range(n):
        lst.append(random.randint(-10 * n, 10 * n))
    return lst


def random_list_positive(n):
    lst = []
    for __ in range(n):
        lst.append(random.randint(0, 10 * n))
    return lst


def test_sort(sort_func, generator=random_list):
    for _ in range(200):
        lst = generator(random.randint(0, 50))
        original = list(lst)
        assert sort_func(lst) == sorted(lst)
        assert lst == original
    print(sort_func.__name__, "OK")


def selection_sort(lst):
    data = list(lst)
    n = len(data)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
    return data


def bubble_sort(lst):
    data = list(lst)
    n = len(data)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def insertion_sort(lst):
    data = list(lst)
    n = len(data)
    for i in range(1, n):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    return data


def measure_avg(sort_func, sizes, generator=random_list):
    avg_times = []
    for n in sizes:
        lst = generator(n)
        total = 0
        for _ in range(3):
            total += time_once(sort_func, lst)
        avg_times.append(total / 3)
    return avg_times


def evaluate(algorithms, sizes, generator=random_list):
    results = {}
    for name, func in algorithms.items():
        results[name] = measure_avg(func, sizes, generator=generator)
    plt.figure()
    for name, avg in results.items():
        plt.plot(sizes, avg, label=name)
    plt.xlabel("list size n")
    plt.ylabel("average time (s)")
    plt.title("Running times")
    plt.legend()

    plt.figure()
    for name, avg in results.items():
        log_x = [math.log2(n) for n in sizes]
        log_y = [math.log2(t) for t in avg]
        m, k = lin_reg(log_x, log_y)
        plt.plot(log_x, log_y, "o", label=f"{name} k = {k:.3f}")
        plt.plot(log_x, [m + k * x for x in log_x], "-")
    plt.xlabel("log2 of list size")
    plt.ylabel("log2 of time")
    plt.title("Log-log plots")
    plt.legend()


def merge_sort(lst):
    if len(lst) <= 1:
        return list(lst)

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(lst):
    if len(lst) <= 1:
        return list(lst)
    pivot = lst[-1]
    rest = lst[:-1]
    smaller = []
    larger = []
    for x in rest:
        if x < pivot:
            smaller.append(x)
        else:
            larger.append(x)
    return quick_sort(smaller) + [pivot] + quick_sort(larger)


def bucket_sort(lst):
    if len(lst) <= 1:
        return list(lst)

    lo = min(lst)
    hi = max(lst)
    if lo == hi:
        return list(lst)
    num_buckets = len(lst)
    buckets = [[] for __ in range(num_buckets)]
    range_size = (hi - lo + 1) / num_buckets
    for x in lst:
        index = int((x - lo) / range_size)
        if index == num_buckets:
            index -= 1
        buckets[index].append(x)
    result = []
    for bucket in buckets:
        sorted_bucket = insertion_sort(bucket)
        result.extend(sorted_bucket)
    return result


def radix_sort(lst):
    if len(lst) <= 1:
        return list(lst)
    data = list(lst)
    max_value = max(data)
    exp = 1
    while max_value // exp > 0:
        data = counting_pass(data, exp)
        exp *= 10
    return data


def counting_pass(data, exp):
    buckets = [[] for __ in range(10)]
    for x in data:
        digit = (x // exp) % 10
        buckets[digit].append(x)
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


def main():
    test_sort(selection_sort)
    test_sort(bubble_sort)
    test_sort(insertion_sort)
    test_sort(merge_sort)
    test_sort(quick_sort)
    test_sort(bucket_sort)
    test_sort(radix_sort, generator=random_list_positive)
    algorithms = {
        "selection": selection_sort,
        "bubble": bubble_sort,
        "insertion": insertion_sort
    }
    nlog_algorithms = {
        "merge": merge_sort,
        "quick": quick_sort,
    }
    special_algorithms = {
        "merge": merge_sort,
        "quick": quick_sort,
        "bucket": bucket_sort,
        "radix": radix_sort,
    }
    sizes = list(range(2000, 12500, 700))
    nlog_sizes = list(range(150000, 1650000, 100000))
    special_sizes = list(range(200000, 1700000, 100000))
    evaluate(algorithms, sizes)
    evaluate(nlog_algorithms, nlog_sizes)
    evaluate(special_algorithms, special_sizes, generator=random_list_positive)
    plt.show()


if __name__ == "__main__":
    main()
