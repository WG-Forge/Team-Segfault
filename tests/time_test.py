import time


def time_test(func, *args):
    start_time = time.time()
    func(args)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.5f} seconds")
