import subprocess
import time
import psutil
import sys
import os

def find_edge_processes():
    """Find all Microsoft Edge processes"""
    edge_processes = []
    edge_names = ['msedge.exe', 'microsoftedge', 'Microsoft Edge', 'edge']
    
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            proc_name = proc.info['name'].lower() if proc.info['name'] else ''
            if any(edge_name in proc_name for edge_name in edge_names):
                edge_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return edge_processes

def open_edge():
    """Open Microsoft Edge based on the operating system"""
    try:
        if sys.platform == "win32":  # Windows
            edge_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                "msedge"  # Try from PATH
            ]
            
            for path in edge_paths:
                try:
                    subprocess.Popen([path], shell=True)
                    return True
                except:
                    continue
            return False
            
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", "-a", "Microsoft Edge"])
            return True
            
        elif sys.platform == "linux":  # Linux
            subprocess.Popen(["microsoft-edge", "microsoft-edge-stable", "edge"], 
                           shell=True)
            return True
        else:
            print(f"Unsupported operating system: {sys.platform}")
            return False
            
    except Exception as e:
        print(f"Error opening Edge: {e}")
        return False

def close_edge():
    """Close all Microsoft Edge processes"""
    try:
        edges_closed = 0
        for proc in find_edge_processes():
            try:
                proc.terminate()  # Graceful termination
                proc.wait(timeout=3)  # Wait for process to end
                edges_closed += 1
            except psutil.TimeoutExpired:
                proc.kill()  # Force kill if not responding
                edges_closed += 1
            except Exception as e:
                print(f"Error closing process {proc.pid}: {e}")
        
        return edges_closed > 0
        
    except Exception as e:
        print(f"Error in close_edge: {e}")
        return False

def main():
    """Main function to open and close Edge infinitely"""
    print("WARNING: This script will open and close Microsoft Edge in an infinite loop!")
    print("Press Ctrl+C to stop the script.\n")
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Open Microsoft Edge
            print("Opening Microsoft Edge...")
            if open_edge():
                print("✓ Microsoft Edge opened successfully")
            else:
                print("✗ Failed to open Microsoft Edge")
                print("Make sure Microsoft Edge is installed on your system")
                break
            
            # Wait a moment for Edge to fully open
            time.sleep(1)
            
            # Close Microsoft Edge
            print("Closing Microsoft Edge.")
            if close_edge():
                print(" Microsoft Edge closed successfully")
            else:
                print("No Microsoft Edge processes found to close")
            
            # Short pause before next iteration
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n Script stopped by user.")
        print(f"Total iterations completed: {iteration}")
        
        # Clean up any remaining Edge processes
        print("Cleaning up remaining Edge processes...")
        close_edge()
        print("Done!")

if __name__ == "__main__":
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("Error: 'psutil' module is required but not installed.")
        print("Please install it using: pip install psutil")
        sys.exit(1)
    
    main()
