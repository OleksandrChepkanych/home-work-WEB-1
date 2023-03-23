import timeit
from multiprocessing import cpu_count, Pool


def factorize(*number):
    results = []
    for n in number:
        result = []
        for i in range(1, n + 1):
            if not n % i:
                result.append(i)
        results.append(result)
    return results


if __name__ == "__main__":
    start_time = timeit.default_timer()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(f"Time standart: {timeit.default_timer() - start_time}")

    start_time = timeit.default_timer()
    with Pool(processes=cpu_count()) as Pool:
        a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(f"Time multiprocessing: {timeit.default_timer() - start_time}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
