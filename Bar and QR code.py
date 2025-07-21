import barcode
from barcode.writer import ImageWriter
import qrcode
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode & QR Code Generator")
        self.root.geometry("800x600")

        # Input frame
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Text:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.text_entry = tk.Entry(input_frame, width=50, font=("Arial", 12))
        self.text_entry.pack(side=tk.LEFT, padx=5)

        # Generate button
        tk.Button(root, text="Generate : ", command=self.generate_codes, font=("Arial", 12)).pack(pady=10)

        # Canvas for displaying images
        self.canvas = tk.Canvas(root, width=700, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Variables to hold image references (prevent garbage collection)
        self.barcode_photo = None
        self.qr_photo = None

    def generate_barcode(self, text, filename):
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(text, writer=ImageWriter())
        barcode_instance.save(filename)
        return f"{filename}.png"

    def generate_qrcode(self, text, filename):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{filename}.png")
        return f"{filename}.png"

    def generate_codes(self):
        text = self.text_entry.get().strip()
        if not text:
            messagebox.showerror("Error", "Please enter some text!")
            return

        # Clear previous images from canvas
        self.canvas.delete("all")

        # Generate unique filenames using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        barcode_filename = f"barcode_{timestamp}"
        qrcode_filename = f"qrcode_{timestamp}"

        try:
            # Generate and save codes
            barcode_path = self.generate_barcode(text, barcode_filename)
            qrcode_path = self.generate_qrcode(text, qrcode_filename)

            # Load and resize images for display
            barcode_img = Image.open(barcode_path)
            barcode_img = barcode_img.resize((300, 150), Image.Resampling.LANCZOS)
            self.barcode_photo = ImageTk.PhotoImage(barcode_img)

            qr_img = Image.open(qrcode_path)
            qr_img = qr_img.resize((150, 150), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(qr_img)

            # Display images on canvas
            self.canvas.create_image(200, 150, image=self.barcode_photo, anchor=tk.CENTER)
            self.canvas.create_image(500, 150, image=self.qr_photo, anchor=tk.CENTER)

            # Add labels
            self.canvas.create_text(200, 50, text="Barcode", font=("Arial", 12))
            self.canvas.create_text(500, 50, text="QR Code", font=("Arial", 12))

            messagebox.showinfo("Success", f"Codes saved as {barcode_filename}.png and {qrcode_filename}.png")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()