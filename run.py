import subprocess
import sys
import time

def run():
    print("Starting Slooze PDF QA Agent...")
    
    try:
        api_process = subprocess.Popen(
            ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8001"],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        print("Backend: http://localhost:8001")
        
        time.sleep(2)
        
        ui_process = subprocess.Popen(
            ["streamlit", "run", "ui/app.py", "--server.port", "8501"],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        print("Frontend: http://localhost:8501")

        api_process.wait()
        ui_process.wait()

    except KeyboardInterrupt:
        print("\nShutting down Slooze PDF QA Agent...")
        api_process.terminate()
        ui_process.terminate()
        api_process.wait()
        ui_process.wait()
        print("Shutdown complete.")

if __name__ == "__main__":
    run()
