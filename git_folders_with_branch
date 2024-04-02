import csv
import os
import subprocess
import sys
import tempfile

def get_git_folders_with_branch(folder_path):
    git_folders = []
    for root, dirs, files in os.walk(folder_path):
        if '.git' in dirs:
            git_folder = os.path.join(root, '.git')
            branch = subprocess.check_output(['git', '-C', git_folder, 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
            changes = subprocess.call(['git', '-C', root, 'diff', '--quiet'])
            git_folders.append((os.path.basename(root), branch, bool(changes)))
    return git_folders

def save_to_temp_csv(git_folders):
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode='w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["Folder", "Branch", "Local Changes"])  # Write header
        for folder, branch, changes in git_folders:
            writer.writerow([folder, branch, "Yes" if changes else "No"])  # Write data rows

    os.startfile(temp_file.name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python git_folders_with_branch <directory_path>")
        sys.exit(1)

    git_folders = get_git_folders_with_branch(sys.argv[1])
    save_to_temp_csv(git_folders)