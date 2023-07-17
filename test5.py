import requests
import tkinter as tk
from tkinter import filedialog
import base64
from tkinter import ttk
from ttkthemes import ThemedTk

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

    # Check if the file exists in the repository
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # File exists, get the current SHA and update the file
        current_content = response.json()
        sha = current_content['sha']
    elif response.status_code == 404:
        # File does not exist, create a new file
        sha = None
    else:
        error_message = response.json().get('message', 'Unknown error')
        result_label.config(text=f"Failed to check file existence. Error: {error_message}", fg="red")
        return

    with open(selected_file_path, "rb") as file:
        content = file.read()
    
    content_base64 = base64.b64encode(content).decode('utf-8')  # Base64 encode the content

    data = {
        "message": commit_message,
        "content": content_base64,  # Use the base64-encoded content in the JSON data
        "branch": branch,
        "sha": sha  # Provide the SHA if it exists, which indicates an update to the existing file
    }

    # Use POST for new file and PUT for updating the existing file
    method = "POST" if sha is None else "PUT"
    response = requests.request(method, url, headers=headers, json=data)

    if response.status_code == 201 or response.status_code == 200:
        result_label.config(text="File uploaded successfully.", fg="green")
    else:
        error_message = response.json().get('message', 'Unknown error')
        result_label.config(text=f"Failed to upload the file. Error: {error_message}", fg="red")


# GUI setup
root = ThemedTk(theme="arc")  # Choose a modern theme ("arc" in this case)
root.title("GitHub File Uploader")
root.geometry("400x300")

label_token = ttk.Label(root, text="Enter GitHub Personal Access Token:")
label_token.pack(pady=5)

entry_token = ttk.Entry(root, show="*")
entry_token.pack(pady=5)

file_label = ttk.Label(root, text="Selected File: ")
file_label.pack(pady=5)

button_select_file = ttk.Button(root, text="Select File", command=select_file)
button_select_file.pack(pady=5)

label_target_path = ttk.Label(root, text="Enter the target path inside the repository:")
label_target_path.pack(pady=5)

entry_target_path = ttk.Entry(root)
entry_target_path.pack(pady=5)

button_send = ttk.Button(root, text="Send", command=upload_to_github)
button_send.pack(pady=10)

result_label = ttk.Label(root, text="", foreground="black")
result_label.pack(pady=5)

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Start the main loop
root.mainloop()
