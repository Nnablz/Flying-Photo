import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Configuration
# Supported image formats
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

# Compatibility for different Pillow versions
try:
    # New Pillow versions (10.0.0+)
    RESAMPLE_MODE = Image.Resampling.LANCZOS
except AttributeError:
    # Older Pillow versions
    try:
        RESAMPLE_MODE = Image.LANCZOS
    except AttributeError:
        RESAMPLE_MODE = Image.ANTIALIAS

class PhotoSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Photo Sorter")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        # State variables
        self.current_folder = ""
        self.image_files = []
        self.current_index = 0
        self.photo_image = None  # Reference to keep image from garbage collection
        self._resize_job = None

        # UI Setup
        self._setup_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', lambda e: self.sort_image('Delete'))
        self.root.bind('<Up>', lambda e: self.sort_image('Maybe'))
        self.root.bind('<Right>', lambda e: self.sort_image('Good'))
        
        # Bind resize event to adjust image size dynamically
        self.root.bind('<Configure>', self._on_resize)

    def _setup_ui(self):
        # 1. Top Control Panel (Packed First)
        control_frame = tk.Frame(self.root, bg="#34495e", pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        btn_select = tk.Button(control_frame, text="Select Folder to Sort", command=self.select_folder, 
                               bg="#3498db", fg="white", font=("Arial", 12, "bold"), padx=20)
        btn_select.pack(side=tk.LEFT, padx=20)

        self.lbl_status = tk.Label(control_frame, text="No folder selected", bg="#34495e", fg="#ecf0f1", font=("Arial", 11))
        self.lbl_status.pack(side=tk.LEFT, padx=20)

        self.lbl_counter = tk.Label(control_frame, text="0 / 0", bg="#34495e", fg="#f1c40f", font=("Arial", 12, "bold"))
        self.lbl_counter.pack(side=tk.RIGHT, padx=20)

        # 2. Bottom Button Panel (Packed SECOND to reserve space at bottom)
        btn_frame = tk.Frame(self.root, bg="#2c3e50", pady=20)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Buttons with corresponding colors
        btn_delete = tk.Button(btn_frame, text="← Delete", command=lambda: self.sort_image('Delete'), 
                               bg="#c0392b", fg="white", font=("Arial", 12, "bold"), width=15)
        btn_delete.pack(side=tk.LEFT, padx=20)

        btn_maybe = tk.Button(btn_frame, text="↑ Maybe", command=lambda: self.sort_image('Maybe'), 
                              bg="#f39c12", fg="white", font=("Arial", 12, "bold"), width=15)
        btn_maybe.pack(side=tk.LEFT, padx=20, expand=True)

        btn_good = tk.Button(btn_frame, text="Good →", command=lambda: self.sort_image('Good'), 
                             bg="#27ae60", fg="white", font=("Arial", 12, "bold"), width=15)
        btn_good.pack(side=tk.RIGHT, padx=20)

        # 3. Main Image Area (Packed LAST to fill remaining space)
        self.image_frame = tk.Frame(self.root, bg="#2c3e50")
        self.image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_image = tk.Label(self.image_frame, bg="#2c3e50", text="Welcome!\nSelect a folder to start sorting.\n\nShortcuts:\nRight Arrow = Good\nUp Arrow = Maybe\nLeft Arrow = Delete", fg="#95a5a6", font=("Arial", 14))
        self.lbl_image.pack(fill=tk.BOTH, expand=True)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self._scan_folder()

    def _scan_folder(self):
        # Find all images in the folder
        try:
            files = os.listdir(self.current_folder)
            self.image_files = [
                f for f in files 
                if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
                and os.path.isfile(os.path.join(self.current_folder, f))
            ]
            
            self.current_index = 0
            
            if not self.image_files:
                messagebox.showinfo("Info", "No images found in this folder!")
                self.lbl_status.config(text="No images found")
            else:
                self.show_current_image()
        except Exception as e:
            messagebox.showerror("Error", f"Could not scan folder: {e}")

    def show_current_image(self):
        if not self.image_files:
            return

        if self.current_index >= len(self.image_files):
            self.lbl_image.config(image='', text="All Done!\nFolder sorting complete.")
            self.lbl_status.config(text="Finished")
            self.lbl_counter.config(text=f"{len(self.image_files)} / {len(self.image_files)}")
            return

        filename = self.image_files[self.current_index]
        filepath = os.path.join(self.current_folder, filename)
        
        # Update status text
        self.lbl_status.config(text=f"Sorting: {filename}")
        self.lbl_counter.config(text=f"{self.current_index + 1} / {len(self.image_files)}")

        try:
            # Load and resize image
            pil_image = Image.open(filepath)
            
            # Calculate aspect ratio to fit in window
            display_width = self.image_frame.winfo_width()
            display_height = self.image_frame.winfo_height()
            
            # Initial startup size fallback
            if display_width < 10: display_width = 800
            if display_height < 10: display_height = 500

            # Resize keeping aspect ratio
            pil_image.thumbnail((display_width, display_height), RESAMPLE_MODE)
            
            self.photo_image = ImageTk.PhotoImage(pil_image)
            self.lbl_image.config(image=self.photo_image, text="")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.lbl_image.config(image='', text=f"Error loading {filename}\nIt might be corrupted.")
            # Auto-skip corrupted files? Uncomment next line to enable:
            # self.sort_image('Skipped_Errors')

    def sort_image(self, category):
        if not self.image_files or self.current_index >= len(self.image_files):
            return

        filename = self.image_files[self.current_index]
        source_path = os.path.join(self.current_folder, filename)
        
        # Create destination folder
        dest_folder = os.path.join(self.current_folder, category)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        dest_path = os.path.join(dest_folder, filename)

        # Handle duplicates: if photo.jpg exists, try photo_1.jpg, photo_2.jpg...
        if os.path.exists(dest_path):
            base, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                new_name = f"{base}_{counter}{extension}"
                dest_path = os.path.join(dest_folder, new_name)
                counter += 1

        try:
            # Move the file
            shutil.move(source_path, dest_path)
            print(f"Moved {filename} to {dest_path}")
            
            # Advance to next image
            self.current_index += 1
            self.show_current_image()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to move file:\n{e}")

    def _on_resize(self, event):
        # Filter events: only care if the image frame itself is resized or the root window
        if event.widget == self.root or event.widget == self.image_frame:
            if hasattr(self, 'image_files') and self.image_files and self.current_index < len(self.image_files):
                if self._resize_job:
                    self.root.after_cancel(self._resize_job)
                self._resize_job = self.root.after(100, self.show_current_image)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PhotoSorterApp(root)
        root.mainloop()
    except Exception as e:
        # Last resort error catching
        print(f"Critical Error: {e}")
        input("Press Enter to close...")