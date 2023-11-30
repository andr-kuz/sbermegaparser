import psutil

def count_process(path: str) -> int:
    processes = []
    for process in psutil.process_iter():
        if path in process.cmdline():
            processes.append(process)
    return len(processes)
