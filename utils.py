import psutil
import os


def count_process(path: str) -> int:
    script_name = path.split(os.sep)[-1]
    path_clear = path.split(script_name)[0][:-1]
    processes = []
    for process in psutil.process_iter():
        try:
            process_path = process.cwd()
        except psutil.AccessDenied:
            continue
        if process_path == path_clear:
            if script_name in process.cmdline():
                processes.append(process)
    return len(processes)
