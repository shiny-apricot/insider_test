import time


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = time.time()

    def start(self):
        self.start_time = time.time()

    def end(self, string):
        self.end_time = time.time()
        print(f"[{string}] Time elapsed: {self.end_time - self.start_time}")
