import requests
import tkinter as tk
from tkinter import filedialog
import base64

selected_file_path = None

def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(title="Select File to Upload")
    if selected_file_path:
        file_label.config(text=f"Selected File: {selected_file_path}")
    else:
        file_label.config(text="Selected File: ")

def upload_to_github():
    global selected_file_path
    if not selected_file_path:
        result_label.config(text="Please select a file.", fg="red")
        return

    token = entry_token.get()
    owner = "OnlineLabProject"
    repo = "OnlineLab"
    branch = "main"  # or the desired branch
    commit_message = "Upload file via API"  # Commit message for the upload
    
    target_path = entry_target_path.get()  # Get the target path from the entry widget
    if not target_path:
        result_label.config(text="Target path cannot be empty.", fg="red")
        return
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{target_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    with open(selected_file_path, "rb") as file:
        content = file.read()
    
    content_base64 = base64.b64encode(content).decode('utf-8')  # Base64 encode the content

    data = {
        "message": commit_message,
        "content": content_base64,  # Use the base64-encoded content in the JSON data
        "branch": branch
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 201:
        result_label.config(text="File uploaded successfully.", fg="green")
    else:
        error_message = response.json().get('message', 'Unknown error')
        result_label.config(text=f"Failed to upload the file. Error: {error_message}", fg="red")

# GUI setup
root = tk.Tk()
root.title("GitHub File Uploader")
root.geometry("400x300")

label_token = tk.Label(root, text="Enter GitHub Personal Access Token:")
label_token.pack()

entry_token = tk.Entry(root, show="*")
entry_token.pack()

file_label = tk.Label(root, text="Selected File: ")
file_label.pack()

button_select_file = tk.Button(root, text="Select File", command=select_file)
button_select_file.pack()

label_target_path = tk.Label(root, text="Enter the target path inside the repository:")
label_target_path.pack()

entry_target_path = tk.Entry(root)
entry_target_path.pack()

button_send = tk.Button(root, text="Send", command=upload_to_github)
button_send.pack()

result_label = tk.Label(root, text="", fg="black")
result_label.pack()

root.mainloop()
