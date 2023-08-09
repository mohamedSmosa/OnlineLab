import tkinter as tk
from tkinter import filedialog
import requests

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        url = entry_url.get()
        with open(file_path, 'rb') as file:
            files = {'file': (file.name, file, 'multipart/form-data')}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                label_status.config(text='File uploaded successfully.')
            else:
                label_status.config(text=f'File upload failed: {response.status_code} {response.text}')

# Create the main application window
app = tk.Tk()
app.title("File Upload GUI")

# URL Entry
label_url = tk.Label(app, text="https://drive.google.com/drive/my-drive")
label_url.pack()
entry_url = tk.Entry(app, width=40)
entry_url.pack()

# Upload Button
btn_upload = tk.Button(app, text="Upload File", command=upload_file)
btn_upload.pack()

# Status Label
label_status = tk.Label(app, text="", fg="green")
label_status.pack()

app.mainloop()
