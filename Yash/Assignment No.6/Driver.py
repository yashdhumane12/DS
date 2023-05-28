from Bully import Bully

# Dummy Processes
process_count = int(input("Enter the number of processes: "))
bully = Bully(process_count)
bully.initializeProcesses()

state = True

while state:
    print("1. Initialize the process\n2. Bring down process\n3. Activate process\n4. Exit\n5. Current Coordinator\n")
    choice = int(input())

    if choice == 1:
        bully.initializeProcesses()

    elif choice == 2:
        crash_id = int(input("Enter the process you want to crash: "))
        bully.crash(crash_id)

    elif choice == 3:
        process_id = int(input("Enter the process you want to start: "))
        bully.start(process_id)

    elif choice == 4:
        state = False
        print("Exiting the program")

    elif choice == 5:
        bully.coordinator()

    else:
        print("Invalid input")
