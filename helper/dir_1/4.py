import os
import git
import time
import stat
import shutil
import requests
from subprocess import call
from datetime import datetime


# Function to clone a repository
def clone_repo(repo_url, clone_dir):
    if not os.path.exists(clone_dir):
        print(f"Cloning repository {repo_url} into {clone_dir}...")
        repo = git.Repo.clone_from(repo_url, clone_dir)
        print("Repository cloned successfully.")
    else:
        print(f"Directory {clone_dir} already exists. Using existing directory.")
        repo = git.Repo(clone_dir)
    return repo

# Function to create a branch using current date and time
def create_branch(repo):
    # Generate a branch name using the current date and time
    branch_name = datetime.now().strftime("branch-%Y-%m-%d_%H-%M-%S")
    main_branch = repo.heads.main
    new_branch = repo.create_head(branch_name, main_branch.commit)
    new_branch.checkout()
    print(f"Branch '{branch_name}' created and checked out.")
    return branch_name

# Function to create or update a README file
def create_readme(repo, file_path, content):
    readme_path = os.path.join(repo.working_tree_dir, file_path)
    if not os.path.exists(readme_path):
        print(f"README file not found. Creating {file_path}...")
        with open(readme_path, 'w') as readme_file:
            readme_file.write(content)
        repo.index.add([file_path])
        print(f"README file '{file_path}' created and added to index.")
    else:
        print(f"README file '{file_path}' already exists.")
    
    # Stage the changes for commit
    repo.index.add([file_path])

# Function to commit and push changes
def commit_and_push(repo, branch_name, commit_message):
    # Commit the changes
    repo.index.commit(commit_message)
    
    # Push the branch to the remote repository and set the upstream
    origin = repo.remotes.origin
    origin.push(branch_name)  # Push the branch to the remote
    repo.heads[branch_name].set_tracking_branch(origin.refs[branch_name])  # Set the upstream branch
    print(f"Changes committed and pushed to branch '{branch_name}'.")

# Function to merge a branch into the main branch
def merge_branch(repo, branch_name):
    main_branch = repo.heads.main
    repo.git.checkout('main')
    repo.git.merge(branch_name)
    print(f"Branch '{branch_name}' merged into 'main'.")

# Function to create a pull request using GitHub API
def create_pull_request(token, repo_owner, repo_name, branch_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/pulls'
    headers = {'Authorization': f'token {token}'}
    pr_data = {
        'title': f'Add README with ML content ({branch_name})',
        'head': branch_name,  # Source branch
        'base': 'main',  # Target branch
        'body': 'This PR adds a README file with machine learning content.',
    }
    
    response = requests.post(url, json=pr_data, headers=headers)
    if response.status_code == 201:
        print(f"Pull request created successfully: {response.json()['html_url']}")
    else:
        print(f"Failed to create pull request: {response.status_code}, {response.text}")


# Handles errors during file removal operations when using shutil.rmtree()
def on_rm_error(func, path, exc_info):
    print(f"PermissionError encountered on {path}. Retrying in 10 seconds...")
    time.sleep(10)
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

# Function to delete the cloned repository directory
def delete_git_file(clone_dir):
    if os.path.exists(clone_dir):
        print(f"Deleting git file {clone_dir}...")
        # Specifically for the .git file
        for i in os.listdir(clone_dir):
            if i.endswith('git'):
                tmp = os.path.join(clone_dir, i)
                # We want to unhide the .git folder before unlinking it.
                while True:
                    call(['attrib', '-H', tmp])
                    break
                shutil.rmtree(tmp, onerror=on_rm_error)
        print(".git file deleted successfully.")
    else:
        print(f"Directory {clone_dir} does not exist.")


# Main function to execute the script
def main():
    repo_url = "https://github.com/Sanmilee/testy.git"
    clone_dir = "auto"
    readme_file = 'README.md'
    readme_content = ("# Machine Learning\n\n" "This is a simple README file for a repository focused on machine learning.\n")

    # Replace with your GitHub token and repository details
    token = os.getenv('GITHUB_TOKEN')
    repo_owner = 'Sanmilee'
    repo_name = 'testy'

    repo = clone_repo(repo_url, clone_dir)
    branch_name = create_branch(repo)  # Create the branch with current date-time as name
    create_readme(repo, readme_file, readme_content)
    commit_and_push(repo, branch_name, 'Add README file with machine learning content')
    create_pull_request(token, repo_owner, repo_name, branch_name)  # Create the PR
    merge_branch(repo, branch_name)

    # Delete git file
    delete_git_file(clone_dir)

if __name__ == "__main__":
    main()
