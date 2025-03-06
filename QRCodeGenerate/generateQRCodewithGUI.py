import qrcode
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

def get_next_available_filename(folder, base_filename, extension):
    # List all files in the folder
    existing_files = os.listdir(folder)
    
    # Filter files with the given base filename and extension
    matching_files = [f for f in existing_files if f.startswith(base_filename) and f.endswith(extension)]
    
    # Extract numbers from the matching files
    numbers = []
    for filename in matching_files:
        try:
            # Extract the number from the filename, assuming it's like 'image_1.png', 'image_2.png', etc.
            number = int(filename[len(base_filename):-len(extension)])
            numbers.append(number)
        except ValueError:
            continue  # Skip files that don't match the expected pattern
    
    # Determine the next available number
    next_number = max(numbers, default=0) + 1
    
    # Construct the new filename
    new_filename = f"{base_filename}{next_number}{extension}"
    
    return new_filename

def generate_qr_code(website_url, folder, bg_color):
    # Define the base filename and extension
    base_filename = "kiri_work_qr_"
    extension = ".png"
    
    # Get the next available filename
    new_filename = get_next_available_filename(folder, base_filename, extension)
    
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # controls the number of pixels for each box
        border=4,  # controls the thickness of the border
    )
    qr.add_data(website_url)
    qr.make(fit=True)
    
    # Create an image from the QR code with the selected background color
    img = qr.make_image(fill='black', back_color=bg_color)
    
    # Save the image with the next available filename
    img.save(os.path.join(folder, new_filename))
    print(f"QR code saved as: {new_filename}")
    return new_filename

# GUI for the QR code generator
def open_gui():
    def browse_folder():
        folder_path = filedialog.askdirectory()  # Prompt for folder selection
        folder_entry.delete(0, tk.END)  # Clear previous folder path
        folder_entry.insert(0, folder_path)  # Insert the selected folder path

    def generate():
        website_url = url_entry.get()  # Get the URL from the entry
        folder_path = folder_entry.get()  # Get the folder path from the entry
        bg_color = color_combobox.get()  # Get the selected background color

        if website_url and folder_path:
            filename = generate_qr_code(website_url, folder_path, bg_color)
            result_label.config(text=f"QR code saved as: {filename}")
        else:
            result_label.config(text="Please fill in all fields!")

    # Set up the main window
    window = tk.Tk()
    window.title("QR Code Generator")

    # URL entry
    tk.Label(window, text="Enter Website URL:").grid(row=0, column=0, padx=10, pady=5)
    url_entry = tk.Entry(window, width=40)
    url_entry.grid(row=0, column=1, padx=10, pady=5)

    # Folder selection (default to current working directory)
    tk.Label(window, text="Select Folder to Save:").grid(row=1, column=0, padx=10, pady=5)
    folder_entry = tk.Entry(window, width=40)
    folder_entry.grid(row=1, column=1, padx=10, pady=5)
    folder_entry.insert(0, os.getcwd())  # Default to current working directory
    browse_button = tk.Button(window, text="Browse", command=browse_folder)
    browse_button.grid(row=1, column=2, padx=10, pady=5)

    # Background color selection
    tk.Label(window, text="Select Background Color:").grid(row=2, column=0, padx=10, pady=5)
    color_combobox = ttk.Combobox(window, values=["white", "yellow", "blue", "green", "red", "black"])
    color_combobox.set("white")  # Default background color
    color_combobox.grid(row=2, column=1, padx=10, pady=5)

    # Generate button
    generate_button = tk.Button(window, text="Generate QR Code", command=generate)
    generate_button.grid(row=3, column=0, columnspan=3, pady=10)

    # Result display
    result_label = tk.Label(window, text="", fg="green")
    result_label.grid(row=4, column=0, columnspan=3, pady=10)

    # Start the GUI
    window.mainloop()

# Run the application
open_gui()
