import subprocess
import signal
import os
import time

# Lista procesów
processes = []

def start_daemon(script_path):
    process = subprocess.Popen(['python3', script_path],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes.append(process)
    return process

def stop_all_processes():
    """function stops all subprocesses"""
    for process in processes:
        os.kill(process.pid, signal.SIGINT)
        time.sleep(2)
        if process.poll() is None:  
            process.terminate() 
            
            
def signal_handler(signum, frame):
    """function handle closing signal"""
    print(f"Received signal {signum}, shutting down...")
    stop_all_processes()
    exit(0)

if __name__ == "__main__":
    #asigining functions to singals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    scripts = ['camera_stream/camera_server.py', 'engines_controler/engine_socketio_host.py', 'control_app/control_host.py']
    print("starting scripts")
    for script in scripts:
        start_daemon(script)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
        stop_all_processes()
