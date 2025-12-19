# Flying-Photo
📸 Fast Photo Sorter ⚡

Sort your photos at the speed of light (or at least, the speed of your thumb).

Tired of dragging and dropping files? Drowning in a sea of "DSC_0001.jpg"?

This app turns the boring chore of organizing photos into a high-speed game. It's like Tinder for your files—but instead of a date, you get a clean hard drive.

🚀 How It Works

Select a Folder: Pick the chaotic folder you want to tame.

The Image Pops Up: Big, clear, and ready for judgment.

Press a Key:

👉 Right Arrow = "GOOD" (Keeper!)

👈 Left Arrow = "DELETE" (Trash it... safely!)

👆 Up Arrow = "MAYBE" (I have commitment issues)

The app automatically creates three folders (Good, Maybe, Delete) and shoots the files into them instantly. No dragging. No clicking. Just pure speed.

✨ Features

Keyboard Warrior Friendly: Keep your hands on the keyboard. No mouse needed.

Safe "Deletion": We don't actually delete your files. We move them to a Delete folder so you can panic-check them later.

Duplicate Destroyer: If photo.jpg already exists, we auto-rename the new one to photo_1.jpg. No crashes.

Tkinter Power: Built with Python's native GUI library. It's ugly but it's fast.

🛠️ Installation & Usage

Option A: The "I am a Coder" Way (Python)

Prerequisites: Python installed.

Clone this repo.

Install the only requirement:

pip install Pillow


Run the script:

python photo_sorter.py


Option B: The "I just want it to work" Way (EXE)

If you built the EXE using the instructions included (PyInstaller):

Go to the dist folder inside your project directory.

Find photo_sorter.exe.

Double click it.

Profit.

🎹 Controls

Key

Action

Destination

→ Right Arrow

Keep it

/Good folder

← Left Arrow

Trash it

/Delete folder

↑ Up Arrow

Unsure

/Maybe folder

🐛 Troubleshooting

"It crashed!": Make sure you have Pillow installed (pip install Pillow).

"The buttons disappeared!": Resize the window slightly, they are shy. (Just kidding, fixed in v1.1).

📝 License

Do whatever you want with this code. Sort photos, sort memes, sort evidence. It's open source!
