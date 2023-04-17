import time


def time_test(func):
    start_time = time.time()
    func()
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.5f} seconds")
