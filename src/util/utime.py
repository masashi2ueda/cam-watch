# %%
import time

class Utime:
    def __init__(self):
        self.st = None
    def start(self):
        self.st = time.time()
    def get_now_sec(self):
        ed = time.time()
        return ed - self.st
    def get_now_min(self):
        return self.get_now_sec() / 60
    def get_now_hour(self):
        return self.get_now_min() / 60
if __name__ == "__main__":
    ut = Utime()
    ut.start()
    time.sleep(1)
    print(ut.get_now_sec())
    print(ut.get_now_min())
    print(ut.get_now_hour())

# %%
