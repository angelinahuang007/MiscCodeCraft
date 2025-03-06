import qrcode
import os

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

def generate_qr_code(website_url, folder):
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
    
    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')
    
    # Save the image with the next available filename
    img.save(os.path.join(folder, new_filename))
    print(f"QR code saved as: {new_filename}")

# Example usage
folder_path = "."  # Replace with the path to your folder
website_url = "https://kiri.work"

generate_qr_code(website_url, folder_path)
