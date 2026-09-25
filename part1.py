import random
import time
import matplotlib.pyplot as plt
import math


def random_list(n):
    lst = []
    for _ in range(n):
        lst.append(random.randint(-10 * n, 10 * n))
    return lst


def threesum_brute(lst, sum=0):
    found = set()
    n = len(lst)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if lst[i] + lst[j] + lst[k] == sum:
                    triple = tuple(sorted((lst[i], lst[j], lst[k])))
                    found.add(triple)
    return sorted(found)


def threesum_pointer(lst, sum=0):
    data = sorted(lst)
    n = len(data)
    found = set()
    for i in range(n - 2):
        lo = i + 1
        hi = n - 1
        while lo < hi:
            total = data[i] + data[lo] + data[hi]
            if total == sum:
                found.add((data[i], data[lo], data[hi]))
                lo += 1
                hi -= 1
            elif total < sum:
                lo += 1
            else:
                hi -= 1
    return sorted(found)


def lin_reg(x, y):
    n = len(x)
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    sum_xx = 0
    for i in range(n):
        sum_x += x[i]
        sum_y += y[i]
        sum_xy += x[i] * y[i]
        sum_xx += x[i] * x[i]
    k = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    m = (sum_y - k * sum_x) / n
    return m, k


def time_once(func, lst):
    start = time.perf_counter()
    func(lst)
    return time.perf_counter() - start


def run_experiment(func, sizes, name):
    runs = [[], [], []]
    for n in sizes:
        print(name, "n =", n)
        for r in range(3):
            runs[r].append(time_once(func, random_list(n)))

    plt.figure()
    plt.plot(sizes, runs[0], "+", label="run 1")
    plt.plot(sizes, runs[1], "x", label="run 2")
    plt.plot(sizes, runs[2], "1", label="run 3")
    plt.xlabel("list size n")
    plt.ylabel("time (s)")
    plt.title("Figure 1: " + name + ", 3 runs")
    plt.legend()

    avg = []
    for i in range(len(sizes)):
        avg.append((runs[0][i] + runs[1][i] + runs[2][i]) / 3)

    plt.figure()
    plt.plot(sizes, avg, "o")
    plt.xlabel("list size n")
    plt.ylabel("average time (s)")
    plt.title("Figure 1a: " + name + ", average of 3 runs")

    log_x = [math.log2(n) for n in sizes]
    log_y = [math.log2(t) for t in avg]
    m, k = lin_reg(log_x, log_y)
    print(name, ": k =", round(k, 3))

    line = [m + k * x for x in log_x]
    plt.figure()
    plt.plot(log_x, log_y, "o", label="data")
    plt.plot(log_x, line, "-", label="fit, k = " + str(round(k, 3)))
    plt.xlabel("log2 of list size")
    plt.ylabel("log2 of time")
    plt.title("Figure 2b: " + name + ", log-log")
    plt.legend()


def correctness_test():
    for _ in range(3):
        lst = random_list(15)
        print("Input:", lst)
        print("Result:", threesum_brute(lst))
        print()


def main():
    correctness_test()

    brute_sizes = list(range(200, 725, 35))
    pointer_sizes = list(range(2000, 11000, 600))

    run_experiment(threesum_brute, brute_sizes, "brute force")
    run_experiment(threesum_pointer, pointer_sizes, "pointer")
    plt.show()


if __name__ == "__main__":
    main()
