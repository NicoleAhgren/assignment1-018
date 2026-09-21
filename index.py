import random


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


def main():
    for _ in range(3):
        lst = random_list(15)
        print("Input:", lst)
        print("Result:", threesum_brute(lst))
        print()


if __name__ == "__main__":
    main()
