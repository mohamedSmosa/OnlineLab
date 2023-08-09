import tkinter as tk
from tkinter import filedialog
from github import Github

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
    repo_name = "OnlineLab"
    branch = "main"  # or the desired branch
    commit_message = "Update file via API"  # Commit message for the upload
    
    target_path = entry_target_path.get()  # Get the target path from the entry widget
    if not target_path:
        result_label.config(text="Target path cannot be empty.", fg="red")
        return

    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    
    try:
        contents = repo.get_contents(target_path)
        existing_content = contents.decoded_content.decode("utf-8")
        with open(selected_file_path, "rb") as file:
            new_content = file.read().decode("utf-8")

        if existing_content == new_content:
            result_label.config(text="File content is up to date.", fg="blue")
        else:
            # Update the file content
            with open(selected_file_path, "rb") as file:
                content = file.read()
            repo.update_file(contents.path, commit_message, content, contents.sha, branch=branch)
            result_label.config(text="File content updated successfully.", fg="green")
    except:
        # File doesn't exist, so we'll create it
        with open(selected_file_path, "rb") as file:
            content = file.read()
        repo.create_file(target_path, commit_message, content, branch=branch)
        result_label.config(text="File uploaded successfully.", fg="green")

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
