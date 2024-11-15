import os
from tkinter import Tk, filedialog, messagebox
from PIL import Image, ImageOps
import ezdxf

def image_to_dxf(input_file, output_file):
    """
    Convert an image to DXF format by tracing its contours.
    
    Args:
        input_file (str): Path to the input PNG file.
        output_file (str): Path to save the output DXF file.
    """
    try:
        # Open the image and convert it to grayscale
        img = Image.open(input_file).convert("L")
        # Convert image to black and white (binary)
        img = img.point(lambda x: 0 if x < 128 else 255, '1')
        
        # Invert the image to have black contours on white background
        img = ImageOps.invert(img.convert("L")).convert("1")

        # Get the width and height of the image
        width, height = img.size

        # Create a new DXF document
        doc = ezdxf.new()
        msp = doc.modelspace()

        # Process image pixels
        pixels = img.load()
        for y in range(height):
            for x in range(width):
                if pixels[x, y] == 0:  # Black pixel
                    # Create a rectangle around the pixel
                    msp.add_lwpolyline([
                        (x, height - y),  # Flip Y-axis for DXF coordinates
                        (x + 1, height - y),
                        (x + 1, height - (y + 1)),
                        (x, height - (y + 1)),
                        (x, height - y)
                    ], close=True)

        # Save the DXF file
        doc.saveas(output_file)
        messagebox.showinfo("Succès", f"Fichier DXF généré : {output_file}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

def process_image():
    """
    Automatically open the file dialog to select an image and process it.
    """
    # Open file dialog to select an image
    input_file = filedialog.askopenfilename(
        title="Sélectionnez une image PNG",
        filetypes=[("Images PNG", "*.png")]
    )
    
    if not input_file:
        messagebox.showwarning("Avertissement", "Aucune image sélectionnée.")
        return

    # Generate output file name
    base, _ = os.path.splitext(input_file)
    output_file = f"{base}_convertie.dxf"

    # Convert the image to DXF
    image_to_dxf(input_file, output_file)

if __name__ == "__main__":
    # Initialize Tkinter without creating a window
    root = Tk()
    root.withdraw()  # Hide the root window

    # Automatically open the file dialog to select an image
    process_image()
