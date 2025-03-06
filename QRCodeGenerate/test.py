import qrcode
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageDraw

# Color mapping for dot colors
COLOR_MAP = {
    "black": (0, 0, 0),
    "yellow": (255, 255, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
}

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

def generate_qr_code(website_url, folder, bg_color, dot_color, style):
    # Define the base filename and extension
    base_filename = "kiri_work_qr_"
    extension = ".png"
    
    # Get the next available filename
    new_filename = get_next_available_filename(folder, base_filename, extension)
    
    # Generate the QR code with the desired style and color
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(website_url)
    qr.make(fit=True)

    # Get the RGB tuple for dot and background color
    dot_color_rgb = COLOR_MAP.get(dot_color, (0, 0, 0))  # Default to black if not found
    bg_color_rgb = COLOR_MAP.get(bg_color, (255, 255, 255))  # Default to white if not found

    # Default style: Square QR Code
    img = qr.make_image(fill=dot_color_rgb, back_color=bg_color_rgb)

    # Apply different styles based on user choice
    if style == "Rounded Dots":
        img = apply_rounded_dots(img, dot_color_rgb)
    elif style == "Separate Squares":
        img = apply_separate_squares(img, dot_color_rgb)

    # Save the image with the next available filename
    img.save(os.path.join(folder, new_filename))
    print(f"QR code saved as: {new_filename}")
    return new_filename

def apply_rounded_dots(img, dot_color):
    """Modify the QR code to have rounded dots."""
    img = img.convert("RGBA")  # Convert to RGBA to allow transparency manipulation
    pixels = img.load()
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == (0, 0, 0, 255):  # Find black pixels (QR code dots)
                # Draw a rounded dot by changing the square to a circle
                pixels[x, y] = dot_color + (255,)  # Set color and full opacity
                
    return img

def apply_separate_squares(img, dot_color):
    """Modify the QR code to use separate squares for each cell."""
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    square_size = 10  # Size of the square cells
    for y in range(0, height, square_size):
        for x in range(0, width, square_size):
            if pixels[x, y] == (0, 0, 0, 255):  # If it's a QR dot
                # Draw a square for each cell instead of the usual dot
                for i in range(x, x + square_size):
                    for j in range(y, y + square_size):
                        if i < width and j < height:
                            pixels[i, j] = dot_color + (255,)
    
    return img

# GUI for the QR code generator
def open_gui():
    def browse_folder():
        folder_path = filedialog.askdirectory()  # Prompt for folder selection
        folder_entry.delete(0, tk.END)  # Clear previous folder path
        folder_entry.insert(0, folder_path)  # Insert the selected folder path

    def generate():
        website_url = url_entry.get()  # Get the URL from the entry
        folder_path = folder_entry.get()  # Get the folder path from the entry
        bg_color = color_combobox_bg.get()  # Get the selected background color
        dot_color = color_combobox_dot.get()  # Get the selected dot color
        style = style_combobox.get()  # Get the selected style

        if website_url and folder_path:
            filename = generate_qr_code(website_url, folder_path, bg_color, dot_color, style)
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
    color_combobox_bg = ttk.Combobox(window, values=["white", "yellow", "blue", "green", "red", "black"])
    color_combobox_bg.set("white")  # Default background color
    color_combobox_bg.grid(row=2, column=1, padx=10, pady=5)

    # Dot color selection
    tk.Label(window, text="Select Dot Color:").grid(row=3, column=0, padx=10, pady=5)
    color_combobox_dot = ttk.Combobox(window, values=["black", "yellow", "blue", "green", "red"])
    color_combobox_dot.set("black")  # Default dot color
    color_combobox_dot.grid(row=3, column=1, padx=10, pady=5)

    # Style selection (QR code style)
    tk.Label(window, text="Select QR Code Style:").grid(row=4, column=0, padx=10, pady=5)
    style_combobox = ttk.Combobox(window, values=["Square", "Rounded Dots", "Separate Squares"])
    style_combobox.set("Square")  # Default style
    style_combobox.grid(row=4, column=1, padx=10, pady=5)

    # Generate button
    generate_button = tk.Button(window, text="Generate QR Code", command=generate)
    generate_button.grid(row=5, column=0, columnspan=3, pady=10)

    # Result display
    result_label = tk.Label(window, text="", fg="green")
    result_label.grid(row=6, column=0, columnspan=3, pady=10)

    # Start the GUI
    window.mainloop()

# Run the application
open_gui()

