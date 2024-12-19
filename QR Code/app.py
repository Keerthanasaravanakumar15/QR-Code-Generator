import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

def generate_qr():
    name = entry_name.get()
    contact = entry_contact.get()
    blood_group = entry_blood_group.get()
    address = entry_address.get()
    emergency_contact = entry_emergency_contact.get()
    
    # Check if all required fields are filled
    if not all([name, contact, blood_group, address, emergency_contact]):
        messagebox.showwarning("Input Error", "Please fill in all fields")
        return
    
    # Format the data to be encoded in the QR code
    data = (
        f"Name: {name}\n"
        f"Contact: {contact}\n"
        f"Blood Group: {blood_group}\n"
        f"Address: {address}\n"
        f"Emergency Contact: {emergency_contact}"
    )
    
    # Generate the QR code
    global qr_image  # Make qr_image global to be accessed by save_qr function
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill='black', back_color='white')
    qr_image.save("qr_code.png")

    # Display the QR code in the GUI
    img = Image.open("qr_code.png")
    
    # Use appropriate resampling method based on Pillow version
    if hasattr(Image, 'Resampling'):
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
    else:
        img = img.resize((200, 200), Image.LANCZOS)

    img = ImageTk.PhotoImage(img)
    qr_label.config(image=img)
    qr_label.image = img

def save_qr():
    # Check if a QR code has been generated
    if qr_image is None:
        messagebox.showwarning("No QR Code", "Please generate a QR code first.")
        return
    
    # Open a file dialog to select save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", ".png"), ("All files", ".*")]
    )
    
    if file_path:
        # Save the QR code image to the specified location
        qr_image.save(file_path)
        messagebox.showinfo("Save Successful", f"QR Code saved to: {file_path}")

# Set up the GUI window
root = tk.Tk()
root.title("Enhanced QR Code Generator")

# Create and place the input fields and labels
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Contact Number:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_contact = tk.Entry(root)
entry_contact.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Blood Group:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_blood_group = tk.Entry(root)
entry_blood_group.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=10, sticky='e')
entry_address = tk.Entry(root)
entry_address.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Emergency Contact:").grid(row=4, column=0, padx=10, pady=10, sticky='e')
entry_emergency_contact = tk.Entry(root)
entry_emergency_contact.grid(row=4, column=1, padx=10, pady=10)

# Create and place the "Generate QR Code" button
generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_button.grid(row=5, columnspan=2, pady=10)

# Create and place the "Download QR Code" button
download_button = tk.Button(root, text="Download QR Code", command=save_qr)
download_button.grid(row=6, columnspan=2, pady=10)

# Label to display the QR code
qr_label = tk.Label(root)
qr_label.grid(row=7, columnspan=2)

# Initialize the global variable for the QR image
qr_image = None

# Start the GUI event loop
root.mainloop()