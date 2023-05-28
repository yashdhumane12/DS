import threading
import time

class TokenRing:
    def __init__(self, numProcesses):
        self.num_processes = numProcesses
        self.threads = []
        self.mutex = threading.Semaphore(1)
        self.tokens = [threading.Event() for _ in range(numProcesses)]
        self.current_token = 0

        for i in range(numProcesses):
            t = threading.Thread(target=self.process, args=(i,))
            self.threads.append(t)

    def start(self):
        for thread in self.threads:
            thread.start()

    def process(self, process_id):
        while True:
            self.tokens[process_id].wait()

            self.mutex.acquire()
            print("Process id:", process_id, "is in critical section.")
            time.sleep(2)
            self.mutex.release()

            print("Process id:", process_id, "is released")

            next_process_id = (process_id + 1) % self.num_processes
            self.tokens[next_process_id].set()

            self.tokens[process_id].clear()

    def initialize_token_ring(self):
        self.tokens[0].set()

if __name__ == "__main__":
    num_processes = 4
    tokenRing = TokenRing(num_processes)
    tokenRing.start()
    tokenRing.initialize_token_ring()
