import subprocess
import os
import sys
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and return True if successful"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Script: {script_name}")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print("SUCCESS")
        if result.stdout:
            print("Output:", result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print("FAILED")
        print("Error:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"SCRIPT NOT FOUND: {script_name}")
        return False

def check_file_exists(filename):
    """Check if a file exists and report size"""
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"File exists: {filename} ({size} bytes)")
        return True
    else:
        print(f"File missing: {filename}")
        return False

def main():
    print("RESTAURANT PIPELINE STARTING")
    print(f"Pipeline started at: {datetime.now()}")
    
    # Step 1: Data Collection
    if not run_script("allareas.py", "Collecting restaurant data from Google Places"):
        print("Pipeline failed at data collection")
        return
    
    # Validate Step 1 output
    if not check_file_exists("unfiltered_rating_restaurants.csv"):
        print("Expected output file not found")
        return
    
    # Step 2: Data Filtering
    if not run_script("rating.py", "Filtering high-rated restaurants"):
        print("Pipeline failed at data filtering")
        return
    
    # Validate Step 2 output
    if not check_file_exists("filtered_rating_restaurants.csv"):
        print("Filtered data file not found")
        return
    
    # Step 3: Map Generation
    if not run_script("map_markers.py", "Generating interactive map"):
        print("Pipeline failed at map generation")
        return
    
    # Validate final output
    if not check_file_exists("high_salvadoran_restaurants_la.html"):
        print("Map file not generated")
        return
    
    print("\nPIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Finished at: {datetime.now()}")
    print("Generated files:")
    print("  - unfiltered_rating_restaurants.csv(raw data)")
    print("  - filtered_rating_restaurants.csv (filtered data)")
    print("  - 'high_salvadoran_restaurants_la.html' (interactive map)")

if __name__ == "__main__":
    main()