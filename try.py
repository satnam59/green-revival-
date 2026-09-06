import tkinter as tk

# Initialize the main window
root = tk.Tk()
root.title("My App")
root.geometry("300x150")

# Define a function to trigger on click
def on_click():
    label.config(text="Button Clicked!")

# Create widgets
label = tk.Label(root, text="Hello, Tkinter!")
button = tk.Button(root, text="Click Me", command=on_click)

# Position widgets
label.pack(pady=10)
button.pack(pady=10)

# Run the event loop
root.mainloop()
