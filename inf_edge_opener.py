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
    """Find Microsoft Edge installation path"""

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


def find_edge_processes():
    """Find all Edge processes"""

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
    """Close Microsoft Edge"""

    processes = find_edge_processes()

    if not processes:
        print("No Edge process found")
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
    print("Running infinitely...")
    print("Press CTRL + C to stop\n")

    iteration = 0

    try:

        while True:

            iteration += 1

            print(f"\n===== CYCLE {iteration} =====")

            print("Opening Edge...")

            if open_edge():
                print("Edge opened")

            else:
                print("Failed to open Edge")
                break

            # Wait for Edge to open
            time.sleep(3)

            print("Closing Edge...")

            if close_edge():
                print("Edge closed")

            else:
                print("No Edge process found")

            # Delay before next cycle
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
        print("psutil not installed.")
        print("Install using:")
        print("pip install psutil")
        sys.exit(1)

    main()
