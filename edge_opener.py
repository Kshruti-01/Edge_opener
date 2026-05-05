import subprocess
import time
import psutil
import sys
import os

# Common Microsoft Edge installation paths
EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

def get_edge_path():
    """Find installed Edge executable"""
    for path in EDGE_PATHS:
        if os.path.exists(path):
            return path
    return None

EDGE_PATH = get_edge_path()

def open_edge():
    """Open Microsoft Edge"""
    try:
        if sys.platform == "win32":

            if not EDGE_PATH:
                print("Microsoft Edge not found!")
                return False

            subprocess.Popen([EDGE_PATH])

        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Microsoft Edge"])

        elif sys.platform == "linux":
            subprocess.Popen(["microsoft-edge-stable"])

        return True

    except Exception as e:
        print(f"Error opening Edge: {e}")
        return False


def find_main_edge_processes():
    """Find only actual Edge browser processes"""

    edge_processes = []

    for proc in psutil.process_iter(['pid', 'name']):

        try:
            proc_name = proc.info['name']

            if proc_name and proc_name.lower() == "msedge.exe":
                edge_processes.append(proc)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    return edge_processes


def close_edge():
    """Close Edge browser"""

    processes = find_main_edge_processes()

    if not processes:
        print("No Edge processes found")
        return False

    closed = 0

    for proc in processes:

        try:
            proc.terminate()

            try:
                proc.wait(timeout=2)

            except psutil.TimeoutExpired:
                proc.kill()

            print(f"Closed PID: {proc.pid}")
            closed += 1

        except Exception:
            pass

    return closed > 0


def main():

    print("=" * 50)
    print("MICROSOFT EDGE OPENER/CLOSER")
    print("=" * 50)

    try:
        cycles = input(
            "Enter number of cycles or 'inf' for infinite: "
        )

        if cycles.lower() == "inf":
            max_iterations = float('inf')
        else:
            max_iterations = int(cycles)

    except ValueError:
        print("Invalid input")
        return

    iteration = 0

    try:

        while iteration < max_iterations:

            iteration += 1

            print(f"\n===== CYCLE {iteration} =====")

            print("Opening Edge...")

            if open_edge():
                print("Edge opened")

            else:
                print("Failed to open Edge")
                break

            time.sleep(3)

            print("Closing Edge...")

            if close_edge():
                print("Edge closed")

            else:
                print("No Edge process found")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user")

    finally:
        close_edge()
        print("Cleanup complete")


if __name__ == "__main__":

    try:
        import psutil

    except ImportError:
        print("Install psutil first:")
        print("pip install psutil")
        sys.exit(1)

    main()
