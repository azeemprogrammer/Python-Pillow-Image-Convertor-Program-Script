import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from tkinter.ttk import Progressbar, Frame, Button, Label, Entry, Scale, Checkbutton, OptionMenu, Style

# Function to convert and compress image to the selected output format
def convert_and_compress(image_path, output_format):
    try:
        image = Image.open(image_path)
        
        # Convert the image to RGB mode if it is in RGBA mode (for JPEG compatibility)
        if image.mode == "RGBA":
            image = image.convert("RGB")
        
        image_output_path = os.path.join(webp_folder.get(), os.path.splitext(os.path.basename(image_path))[0] + "." + output_format)
        image.save(image_output_path, format=output_format)
        if delete_original.get():
            os.remove(image_path)
        return image_output_path
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return ""

# Function to handle the conversion button click
def convert_button_click():
    jpg_folder_path = jpg_folder.get()
    webp_folder_path = webp_folder.get()
    input_format = selected_input_format.get()
    output_format = selected_output_format.get()
    
    image_files = [file for file in os.listdir(jpg_folder_path) if file.lower().endswith("." + input_format)]

    if not image_files:
        status_label["text"] = f"No {input_format} images found in the folder."
        return

    progress_bar["maximum"] = len(image_files)
    progress_bar["value"] = 0
    status_label["text"] = "Converting..."

    for i, file in enumerate(image_files):
        image_path = os.path.join(jpg_folder_path, file)
        output_path = convert_and_compress(image_path, output_format)
        if output_path:
            print(f"Converted {image_path} to {output_path}")
        progress_bar["value"] = i + 1
        window.update()

    status_label["text"] = "Conversion complete."

# Function to handle the browse buttons for folder selection
def browse_jpg_folder():
    folder_path = filedialog.askdirectory()
    jpg_folder.delete(0, END)
    jpg_folder.insert(0, folder_path)

def browse_webp_folder():
    folder_path = filedialog.askdirectory()
    webp_folder.delete(0, END)
    webp_folder.insert(0, folder_path)

# Create the main window
window = Tk()
window.title("Image Converter")
window.geometry("400x400")
window.resizable(False, False)

# Set window icon

# Create a style for the window
style = Style()
style.configure("TFrame", background="#f2f2f2")
# style.configure("TButton", background="green", foreground="white")
style.configure("TCheckbutton", background="#f2f2f2")
style.configure("TProgressbar", background="#007bff", troughcolor="#f2f2f2")

# Create a frame
frame = Frame(window, style="TFrame")
frame.pack(pady=20)

# Create a dropdown menu for input format selection
supported_input_formats = ["jpg", "png", "bmp", "eps", "gif", "ico", "im", "jpeg", "msp", "pcx", "ppm", "sgi", "spi", "tiff", "webp", "xv", "gif", "mpo", "pdf"]
selected_input_format = StringVar()
selected_input_format.set(supported_input_formats[0])

input_format_label = Label(frame, text="Input Format:")
input_format_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")

input_format_dropdown = OptionMenu(frame, selected_input_format, *supported_input_formats)
input_format_dropdown.grid(row=0, column=1, pady=5, padx=10, sticky="we")

# Create a dropdown menu for output format selection
supported_output_formats = ["jpg", "png", "bmp", "eps", "gif", "ico", "im", "jpeg", "msp", "pcx", "ppm", "sgi", "spi", "tiff", "webp", "xv", "gif", "mpo", "pdf"]
selected_output_format = StringVar()
selected_output_format.set(supported_output_formats[0])

output_format_label = Label(frame, text="Output Format:")
output_format_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")

output_format_dropdown = OptionMenu(frame, selected_output_format, *supported_output_formats)
output_format_dropdown.grid(row=1, column=1, pady=5, padx=10, sticky="we")

# Create input fields for jpg and output folders
jpg_folder_label = Label(frame, text="JPG Folder:")
jpg_folder_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")

jpg_folder = Entry(frame)
jpg_folder.grid(row=2, column=1, pady=5, padx=10, sticky="we")

jpg_folder_button = Button(frame, text="Browse", command=browse_jpg_folder)
jpg_folder_button.grid(row=2, column=2, pady=5, padx=10)

webp_folder_label = Label(frame, text="Output Folder:")
webp_folder_label.grid(row=3, column=0, pady=5, padx=10, sticky="w")

webp_folder = Entry(frame)
webp_folder.grid(row=3, column=1, pady=5, padx=10, sticky="we")

webp_folder_button = Button(frame, text="Browse", command=browse_webp_folder)
webp_folder_button.grid(row=3, column=2, pady=5, padx=10)

# Create a checkbox for deleting original files
delete_original = BooleanVar()
delete_checkbox = Checkbutton(frame, text="Delete original files", variable=delete_original, style="TCheckbutton")
delete_checkbox.grid(row=4, column=1, pady=5, padx=10, sticky="w")

# Create a button to start the conversion
convert_button = Button(frame, text="Convert", command=convert_button_click, style="TButton")
convert_button.grid(row=5, column=1, pady=10, padx=10, sticky="we")

# Create a progress bar
progress_bar = Progressbar(window, length=300, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=20)

# Create a label for status message
status_label = Label(window, text="", font=("Helvetica", 12), background="#f2f2f2")
status_label.pack()

# Run the GUI main loop
window.mainloop()
