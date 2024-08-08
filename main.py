import os
import time
import threading
import random
import ctypes



tasks = {}

exit_flags = {}

task_progress = {}

def printTaskList():
    print("----------------------------")
    for task_id, task_info in tasks.items():
        print(f"Task ID: {task_id}")
        print(f"Thread Name: {task_info['thread'].name}")
        print(f"Task Name: {task_info['name']}")
        print(f"Thread Daemon: {task_info['thread'].daemon}")
        print(f"Thread Alive: {task_info['thread'].is_alive()}")

        if task_info['thread'].name in task_progress:
            progress = task_progress[task_info['thread'].name]
            bar_width = 25  # Adjust the width of the progress bar
            bar = '#' * int(bar_width * (progress / 100))
            spaces = ' ' * (bar_width - len(bar))
            print(f"Progress: [{bar}{spaces}] {progress:.2f}%")
        print("----------------------------------")

def printAliveTaskList():
    print("----------------------------")
    for task_id, task_info in tasks.items():
        if task_info['thread'].is_alive():
            print(f"Task ID: {task_id}")
            print(f"Thread Name: {task_info['thread'].name}")
            print(f"Task Name: {task_info['name']}")
            print(f"Thread Daemon: {task_info['thread'].daemon}")
            print(f"Thread Alive: {task_info['thread'].is_alive()}")
            # Display progress bar
            if task_info['thread'].name in task_progress:
                progress = task_progress[task_info['thread'].name]
                bar_width = 25  # Adjust the width of the progress bar
                bar = '#' * int(bar_width * (progress / 100))
                spaces = ' ' * (bar_width - len(bar))
                print(f"Progress: [{bar}{spaces}] {progress:.2f}%")
            else:
                progress = 0
                print(f"Progress: [ Initializing... ] {progress:.2f}%")
            print("----------------------------------")
    print("==================================")
    if len(task_progress) > 0:
        progress = sum(task_progress.values()) / len(task_progress)
        bar_width = 25
        bar = '#' * int(bar_width * (progress / 100))
        spaces = ' ' * (bar_width - len(bar))
        print(f"Total Progress: [{bar}{spaces}] {progress:.2f}%")
        print("==================================")


def clear_console():
    os.system('cls')

def showMainMenu():
    print("Console Menu:")
    print("1. Tasks")
    print("2. Show Tasks History")
    print("3. Show Alive Tasks")
    print("4. Kill Task")
    print("5. Exit")

def showTasksMenu():
    clear_console()
    print("\nTasks Menu:")
    print("1. Find n-th prime number")
    print("2. Task simulation")
    print("3. Approximate value of π")
    print("4. Max knapsack value")
    print("5. Back to main menu")

def performTasks(option):
    if option == 1:
        try:
            userInput = int(input("Enter the position of the prime number you want to find: "))
            if userInput <= 0:
                print("Please enter a number greater than zero.")
            else:
                print(f"Looking for {userInput}th prime number...")
                addTask(f"{userInput} prime number", findNthPrimeNumber, (userInput,))
        except ValueError:
            print("Please enter a valid integer.")

    elif option == 2:
        try:
            task_name = input("Enter task name: ")
            duration_seconds = int(input("Enter duration in seconds (E.g. 30): "))
            print(f"Performing Task: {task_name}")
            addTask(f"{task_name} - duration: {duration_seconds}", taskSimulation,
                    (task_name, duration_seconds,))
        except ValueError:
            print("Please enter a valid integer.")

    elif option == 3:
        try:
            num_points = int(input("Enter the number of points to be drawn: (E.g. 1000000): "))
            if num_points <= 0:
                print("Please enter a number greater than zero.")
            else:
                print(f" Estimating the value of pi having {num_points} points...")
                addTask(f"monte carlo {num_points} points", piApproximation, (num_points,))
        except ValueError:
            print("Please enter a valid integer.")

    elif option == 4:
        try:
            size = int(input("Enter number of weights/values: "))
            capacity = int(input("Enter knapsack capacity (E.g. 10000)"))
            print(f"Calculating max value of knapsack with {capacity} capacity")
            addTask(f"Knapsack {capacity} capacity", knapsacCalculation,
                    (capacity, size,))
        except ValueError:
            print("Please enter a valid integer.")

    elif option == 5:
        clear_console()
        main()
    else:
        clear_console()
        print("Invalid option. Please choose a valid option.\n")


def findNthPrimeNumber(exit_flag, userInput):
    result = nthPrimeNumber(userInput)
    if userInput > 30000:
        print(f"\n{userInput}-th prime number is: {result}")
    else:
        time.sleep(2)
        print(f"\n{userInput}-th prime number is: {result}")
    while True:
        if exit_flag.is_set():
            print(f"Thread {threading.current_thread().name} is stopping.")
            return
        time.sleep(1)
        break

def nthPrimeNumber(n):
    progress = 0
    task_progress[threading.current_thread().name] = progress
    count = 0
    num = 2
    while True:
        if isPrime(num):
            progress = count / n * 100
            task_progress[threading.current_thread().name] = progress
            count += 1
            if count == n:
                return num
        num += 1

def isPrime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def taskSimulation(exit_flag, task_name, duration_seconds):
    progress = 0
    task_progress[threading.current_thread().name] = progress
    print(f"Started task: {task_name}")

    for x in range(duration_seconds):
        if exit_flag.is_set():
            print(f"Thread {threading.current_thread().name} is stopping.")
            return
        time.sleep(1)
        # Update progress
        progress = int((x + 1) / duration_seconds * 100)
        task_progress[threading.current_thread().name] = progress

    print(f"\nTask simulation: {task_name} has been finished")

def piApproximation(exit_flag, num_points):
    estimated_pi = calculatePi(num_points)
    print(f"Przybliżona wartość liczby π: {estimated_pi}")
    while True:
        if exit_flag.is_set():
            print(f"Thread {threading.current_thread().name} is stopping.")
            return
        time.sleep(1)
        break

def calculatePi(num_points):
    progress = 0
    task_progress[threading.current_thread().name] = progress
    points_inside_circle = 0
    for i in range(num_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)

        distance = x ** 2 + y ** 2

        if distance <= 1:
            points_inside_circle += 1
            progress = i / num_points * 100
            task_progress[threading.current_thread().name] = progress

    return (points_inside_circle / num_points) * 4

def knapsacCalculation(exit_flag, capacity, size):
    task_progress[threading.current_thread().name] = 0
    rngW = random.randint(1, 20)
    rngV = random.randint(1, 20)
    weights = [i * rngW for i in range(1, size + 1)]
    values = [i * rngV for i in range(1, size + 1)]
    start_time = time.time()
    max_value = knapsackValue(weights, values, capacity)
    end_time = time.time()
    print("\nweights: ", weights)
    print("values:  ", values)
    print(f"Max knapsack value with capacity of {capacity}: {max_value}")
    print(f"Execution time: {end_time - start_time} seconds")
    while True:
        if exit_flag.is_set():
            print(f"Thread {threading.current_thread().name} is stopping.")
            return
        time.sleep(1)
        break

def knapsackValue(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    progress = 1 / n * 100
    task_progress[threading.current_thread().name] = progress

    for i in range(1, n + 1):
        progress = i / n * 100
        task_progress[threading.current_thread().name] = progress
        for w in range(capacity + 1):
            progress = i / n * 100
            task_progress[threading.current_thread().name] = progress
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

def main():
    global task_progress
    task_progress = {}
    while True:
        showMainMenu()
        try:
            option = int(input("Enter your choice (1-5): "))
            if option == 1:
                while True:
                    clear_console()
                    showTasksMenu()
                    try:
                        task_option = int(input("Enter your task choice (1-5): "))
                        performTasks(task_option)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

            elif option == 2:
                printTaskList()

            elif option == 3:
                printAliveTaskList()

            elif option == 4:
                if len(tasks)>0:
                    print("Current Tasks:")
                    printAliveTaskList()
                    task_id = int(input("Enter the ID of the task you want to delete: "))
                    deleteTask(task_id)
                else:
                    print("No alive tasks found")

            elif option == 5:
                print("Exiting the program. Goodbye!")
                exit()

            else:
                clear_console()
                print("Invalid option. Please choose a valid option.\n")
        except ValueError:
            print("Invalid input. Please enter a number.")

def addTask(name, target_function, args):
    while True:
        task_id = random.randint(1000, 25000)
        if task_id not in tasks:
            break
    exit_flag = threading.Event()
    exit_flags[task_id] = exit_flag

    thread = threading.Thread(target=target_function, args=(exit_flag,) + args)
    thread.name = name
    thread.daemon = True
    tasks[task_id] = {"name": name, "thread": thread, "exit_flag": exit_flag}
    thread.start()

def deleteTask(task_id):
    if task_id in tasks:
        thread_info = tasks[task_id]
        exit_flag = thread_info["exit_flag"]
        thread = thread_info["thread"]

        exit_flag.set()
        terminateThread(thread)

        thread.join()

        if not thread.is_alive():
            tasks.pop(task_id)
            exit_flags.pop(task_id)
            if thread.name in task_progress:
                task_progress.pop(thread.name)
            print(f"Thread id:'{task_id}'")
        else:
            print(f"Thread id:'{task_id}' is still running and cannot be deleted.")
    else:
        print(f"Task with ID {task_id} not found.")

def terminateThread(thread):
    """Thread terminating"""
    if not thread.is_alive():
        return

    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(thread_id), ctypes.py_object(SystemExit))

    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print(f"Thread '{thread.name}' terminated forcibly.")
    else:
        print(f"Thread '{thread.name}' terminated gracefully.")

if __name__ == "__main__":
    mainThread = threading.Thread(target=main)
    mainThread.name = "Menu"
    mainThread.start()
