import tkinter as tk
from tkinter import filedialog
import re

def remove_asterisks_and_numbers(input_file, output_file):
    # Read the contents of the input file
    with open(input_file, 'r') as file:
        content = file.read()

    # Remove all asterisks (*)
    modified_content = content.replace('*', '')

    # Remove numbers and adjacent dots using regex
    # This regex matches numbers followed by a dot (e.g., "43.") or just numbers (e.g., "43")
    modified_content = re.sub(r'\d+\.?', '', modified_content)

    # Write the modified content to the output file
    with open(output_file, 'w') as file:
        file.write(modified_content)

    print(f"Processed content saved to '{output_file}'.")

def select_file():
    # Create a Tkinter root window (it will be hidden)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to select the input file
    input_file = filedialog.askopenfilename(
        title="Select the input file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not input_file:
        print("No input file selected. Exiting.")
        return

    # Ask the user to specify the output file
    output_file = filedialog.asksaveasfilename(
        title="Save the output file as",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not output_file:
        print("No output file specified. Exiting.")
        return

    # Call the function to remove asterisks and numbers
    remove_asterisks_and_numbers(input_file, output_file)

# Run the file dialog
select_file()