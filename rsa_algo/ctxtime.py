import time

class Timer:

    def __init__(self):
        self.start = 0
        self.end = 0


    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.end = time.time() - self.start
        print(f"time: {self.end}")
