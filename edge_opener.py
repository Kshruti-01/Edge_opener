import subprocess
import time
import psutil
import sys
import os

def open_edge():
    """Open Microsoft Edge"""
    try:
        if sys.platform == "win32":
            subprocess.Popen(["msedge"], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Microsoft Edge"])
        elif sys.platform == "linux":
            subprocess.Popen(["microsoft-edge-stable"])
        return True
    except Exception as e:
        print(f"Error opening Edge: {e}")
        return False

def find_main_edge_processes():
    """Find ONLY the main Microsoft Edge browser processes"""
    edge_processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            proc_name = proc.info['name'].lower() if proc.info['name'] else ''
            cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''
            
            # Only target main Edge browser processes
            if proc_name == 'msedge.exe':
                # Exclude updater and other helper processes
                is_updater = 'update' in cmdline or 'MicrosoftEdgeUpdate' in proc_name
                is_webview2 = 'webview2' in cmdline or 'webview' in proc_name
                is_crashpad = 'crashpad' in cmdline
                
                # Only kill actual browser windows
                if not is_updater and not is_webview2 and not is_crashpad:
                    edge_processes.append(proc)
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
            
    return edge_processes

def close_edge():
    """Close only main Edge browser windows"""
    try:
        processes = find_main_edge_processes()
        
        if not processes:
            print(" No main Edge browser processes found")
            return False
        
        edges_closed = 0
        for proc in processes:
            try:
                # Try graceful close first
                proc.terminate()
                proc.wait(timeout=2)
                print(f"Closed Edge process (PID: {proc.pid})")
                edges_closed += 1
            except psutil.TimeoutExpired:
                # Force kill if not responding
                proc.kill()
                print(f"Force killed Edge process (PID: {proc.pid})")
                edges_closed += 1
            except Exception as e:
                print(f"Error: {e}")
                
        return edges_closed > 0
        
    except Exception as e:
        print(f"Error in close_edge: {e}")
        return False

def main():
    print("="*50)
    print("MICROSOFT EDGE OPENER/CLOSER")
    print("="*50)
    print("This will open and close Edge browser windows")
    print("Press Ctrl+C to stop\n")
    
    # Safety: Ask for confirmation
    try:
        confirm = input("How many cycles? (enter number or 'inf' for infinite): ")
        if confirm.lower() == 'inf':
            max_iterations = float('inf')
            print("Running infinitely until Ctrl+C...\n")
        else:
            max_iterations = int(confirm)
            print(f"Running {max_iterations} cycles...\n")
    except ValueError:
        print("Invalid input. Exiting.")
        return
    
    iteration = 0
    
    try:
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'='*30}")
            print(f"CYCLE {iteration}")
            print(f"{'='*30}")
            
            # Open Edge
            print("Opening Edge.")
            if open_edge():
                print("Edge opened successfully")
            else:
                print("Failed to open Edge")
                break
            
            # Wait for Edge to fully open
            time.sleep(2)
            
            # Close Edge
            print("Closing Edge.")
            if close_edge():
                print("Edge closed successfully")
            else:
                print("No Edge windows to close")
            
            # Pause between cycles
            if iteration < max_iterations:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print(f"\n\nSTOPPED by user after {iteration} cycles")
        
    finally:
        # Final cleanup
        print("\nCleaning up")
        close_edge()
        print("Done!")

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("'psutil' not installed. Install with: pip install psutil")
        sys.exit(1)
    
    main()


PS C:\Users\850085869\OneDrive - Genpact\Desktop\Project\edge_opener> python test_edge.py
==================================================
MICROSOFT EDGE OPENER/CLOSER
==================================================
This will open and close Edge browser windows
Press Ctrl+C to stop

How many cycles? (enter number or 'inf' for infinite): 10
Running 10 cycles...


==============================
CYCLE 1
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
Closed Edge process (PID: 15196)
Closed Edge process (PID: 16224)
Closed Edge process (PID: 16572)
Error: process no longer exists (pid=20700, name='msedge.exe')
Error: process no longer exists (pid=23828, name='msedge.exe')
Edge closed successfully

==============================
CYCLE 2
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 3
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 4
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 5
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 6
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 7
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 8
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 9
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

==============================
CYCLE 10
==============================
Opening Edge.
Edge opened successfully
'msedge' is not recognized as an internal or external command,
operable program or batch file.
Closing Edge.
 No main Edge browser processes found
No Edge windows to close

Cleaning up
 No main Edge browser processes found
Done!
