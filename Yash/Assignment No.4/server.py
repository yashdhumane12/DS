import threading
import datetime
import socket
import time
from dateutil import parser

# Client data to be stored in the variable client_data
client_data = {}

# Nested thread function used to receive clock time from a connected client
def startReceivingClockTime(connector, address):
    while True:
        # receive clock time
        clock_time_string = connector.recv(1023).decode()
        clock_time = parser.parse(clock_time_string)
        clock_time_diff = datetime.datetime.now() - clock_time
        client_data[address] = {
            "clock_time": clock_time,
            "time_difference": clock_time_diff,
            "connector": connector
        }
        print("Client data updated with: " + str(address), end="\n\n")
        time.sleep(5)

# This opens up the master server to accept clients over a given port
def startConnecting(master_server):
    # Fetching clock time at slaves/clients
    while True:
        master_slave_connector, addr = master_server.accept()
        slave_address = str(addr[0]) + ":" + str(addr[1])
        print(slave_address + " got connected successfully")

        current_thread = threading.Thread(
            target=startReceivingClockTime,
            args=(master_slave_connector, slave_address,)
        )
        current_thread.start()

# Used to fetch average clock difference
def getAverageClockDiff():
    current_client_data = client_data.copy()
    time_difference_list = list(client['time_difference'] for clientadd, client in current_client_data.items())
    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta(0, 0))
    average_clock_difference = sum_of_clock_difference / len(current_client_data)
    return average_clock_difference

# Master sync thread function used to generate cycles of clock synchronization in the network
def synchronizeAllClocks():
    while True:
        print("New synchronization cycle started.")
        print("Number of clients to be synchronized: " + str(len(client_data)))

        if len(client_data) > 0:
            average_clock_difference = getAverageClockDiff()

            for client_addr, client in client_data.items():
                try:
                    synchronized_time = datetime.datetime.now() + average_clock_difference
                    client["connector"].send(str(synchronized_time).encode())

                except Exception as e:
                    print("Something went wrong while sending synchronized time through " + str(client_addr))

        else:
            print("No client data. Synchronization not applicable.")

        print("\n\n")
        time.sleep(5)

def initiateClockServer(port=8080):
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket at master node created successfully")

    HOST = "127.0.0.1"
    master_server.bind((HOST, port))

    # Starts listening to requests
    master_server.listen(10)
    print("Clock server started...")

    # Start making connections
    print("Starting to make connections...")
    master_thread = threading.Thread(
        target=startConnecting,
        args=(master_server,)
    )
    master_thread.start()

    # Start synchronization
    print("Starting synchronization in parallel...")
    sync_thread = threading.Thread(
        target=synchronizeAllClocks,
        args=()
    )
    sync_thread.start()

# Driver function
if __name__ == '__main__':
    # Trigger the Clock Server
    initiateClockServer(port=8080)
