import csv
from datetime import datetime
import sys
def purge_log_file(input_str, output_file, error_file):
     # Read input from file
    with open(input_file, 'r') as file:
        input_str = file.read()
    # Split the input string into lines
    lines = input_str.split('\n')

    # Initialize variables
    success = 0
    failed = 0
    package_success = 0
    package_failed = 0

    # Process each line
    for line in lines:
        line = line.strip()
        if line.startswith("Total 4G provision Success:"):
            success = line.split(": ")[-1]
        elif line.startswith("Total 4G provision Failed:"):
            failed = line.split(": ")[-1]
        elif line.startswith("Total 4G Package Success:"):
            package_success = line.split(": ")[-1]
        elif line.startswith("Total 4G Package Failed:"):
            package_failed = line.split(": ")[-1]
        # Validate values
    if success == '' or failed == '' or package_success == '' or package_failed == '':
        # Write error message to output file
        with open(error_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Error: Invalid log format'])
        # Exit the program
        sys.exit("Error: Invalid log format")

    # Write output to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([success, failed, package_success, package_failed])

# Example usage
file_date= datetime.now().strftime("%Y%m%d")
input_file = f"D:\DBA\python\code\Python_test\TR_26_daily_count_report_{file_date}.txt"
output_file = f"D:\DBA\python\code\Python_test\TR_26_daily_count_report_{file_date}.csv"
error_file = f"D:\DBA\python\code\Python_test\TR_26_daily_count_error_report_{file_date}.csv"
#sample_input = '''Total 4G provision Success: 290401
#Total 4G provision Failed: 0
#Total 4G Package Success: 308512
#Total 4G Package Failed: 126'''

purge_log_file(input_file, output_file,error_file)
