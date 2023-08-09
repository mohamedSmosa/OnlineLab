
'''
elkholy
import requests

def upload_file_to_github(repo_owner, repo_name, file_path, file_contents, branch, access_token):
    #base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    base_url = f"https://github.com/OnlineLabProject/OnlineLab/blob/main/New%20Text%20Document.txt"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "message": "Upload file via Python script",
        "content": file_contents,
        "branch": branch
    }

    response = requests.put(base_url, json=data, headers=headers)

    if response.status_code == 201:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}, Error: {response.json()}")

if __name__ == "__main__":
    # GitHub repository details
    repo_owner = "OnlineLabProject"  # Replace with your GitHub username or organization name
    repo_name = "OnlineLab"   # Replace with the name of your GitHub repository
    file_path = "/OnlineLabProject/OnlineLab/main/file.txt" # Replace with the path where you want to upload the file in the repository
    branch = "main"                    # Replace with the name of the branch you want to upload the file to

    # File contents
    with open("your_file.txt", "r") as file:
        file_contents = file.read()

    # GitHub personal access token
    access_token = "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"  # Replace with your generated personal access token

    upload_file_to_github(repo_owner, repo_name, file_path, file_contents, branch, access_token)
'''


import requests
import tkinter as tk
from tkinter import filedialog

def get_file_content_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text
        return content
    else:
        print(f"Failed to fetch file content. Status code: {response.status_code}")
        return None

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r") as file:
            file_content = file.read()
        if file_content:
            print("File content:")
            print(file_content)

            # Fetch content from GitHub link
            github_url = "https://raw.githubusercontent.com/OnlineLabProject/OnlineLab/main/New%20Text%20Document.txt"
            github_content = get_file_content_from_github(github_url)
            if github_content:
                print("GitHub File content:")
                print(github_content)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Chooser")

    button = tk.Button(root, text="Choose File", command=browse_file)
    button.pack(pady=20)

    root.mainloop()
