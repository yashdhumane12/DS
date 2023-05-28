from statistics import mode

class Process:
    def __init__(self, process_id, total_count):
        self.process_id = process_id
        self.total_count = total_count
        self.leader_id = -1
        self.is_active = True

    def crash(self):
        self.is_active = False

    def start(self):
        self.is_active = True

    def is_leader(self):
        if self.process_id == self.leader_id:
            return True
        return False

    def set_leader(self, leader):
        self.leader_id = leader

    def get_leader(self):
        return self.leader_id

    def sendRequest(self, toProcess):
        print(f"Sending request to process {toProcess.process_id} from {self.process_id}")
        if toProcess.reciveRequest(self.process_id):
            print(f"Ok received from {toProcess.process_id}")
            self.set_leader(toProcess.process_id)
        else:
            print(f"No response from {toProcess.process_id}")

    def reciveRequest(self, fromProcess):
        if self.is_active:
            print(f"Received request from process {fromProcess}.")
            return self.recivedMessage()
        return False

    def recivedMessage(self):
        return True


class Bully:
    def __init__(self, total_count):
        self.processes = []
        self.total_count = total_count

    def initializeProcesses(self):
        self.processes = []
        for i in range(self.total_count):
            self.processes.append(Process(i, total_count=self.total_count))
        self.elect_leader()
        self.coordinator()

    def elect_leader(self, current=0):
        for i in range(current, self.total_count):
            if self.processes[i].is_active:
                for j in range(i + 1, self.total_count):
                    if self.processes[j].is_active:
                        self.processes[i].sendRequest(self.processes[j])
                    elif not self.processes[j].is_active and i + 1 == self.total_count - 1:
                        self.processes[i].sendRequest(self.processes[i])

            if self.processes[i].get_leader() == -1:
                self.processes[i].sendRequest(self.processes[i])

    def crash(self, crash_id):
        if 0 <= crash_id < self.total_count:
            self.processes[crash_id].crash()
            if self.processes[crash_id].is_leader():
                print("Leader process down. Initializing the leader election.")
                self.elect_leader(0)

    def start(self, process_id):
        if self.processes[process_id].is_active:
            print("Process already active")
        else:
            self.processes[process_id].start()
            self.elect_leader()

    def coordinator(self):
        leader = []
        for p in self.processes:
            if p.is_active:
                print(p.get_leader())
                leader.append(p.get_leader())

        self.leader = mode(leader)
