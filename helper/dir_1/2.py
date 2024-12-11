import os
import git
from datetime import datetime


# Token
# https://github.com/settings/tokens

# Setting Environment Variables:
# set GITHUB_TOKEN=your_personal_access_token


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

# Function to create a branch from the main branch
def create_branch(repo):
    # Generate a branch name using the current date and time
    branch_name = datetime.now().strftime("branch-%Y-%m-%d_%H-%M-%S")
    main_branch = repo.heads.main
    new_branch = repo.create_head(branch_name, main_branch.commit)
    new_branch.checkout()
    print(f"Branch '{branch_name}' created and checked out.")

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
        with open(readme_path, 'w') as readme_file:
            readme_file.write(content)
        repo.index.add([file_path])
        print(f"Add new texts to README file")
    
    # Stage the changes for commit
    repo.index.add([file_path])

# Function to commit and push changes
def commit_and_push(repo, branch_name, commit_message):
    repo.index.commit(commit_message)
    origin = repo.remotes.origin
    origin.push(branch_name)
    print(f"Changes committed and pushed to branch '{branch_name}'.")

# Function to merge a branch into the main branch
def merge_branch(repo, branch_name):
    main_branch = repo.heads.main
    repo.git.checkout('main')
    repo.git.merge(branch_name)
    print(f"Branch '{branch_name}' merged into 'main'.")

# Main function to execute the script
def main(repo_url, clone_dir):
    repo_url = "https://github.com/Sanmilee/testy.git"
    clone_dir = "auto"
    readme_file = 'README.md'
    readme_content = ("# Machine Learning\n\n" "This is a simple README file for a repository focused on machine learning.\n")

    # Replace with your GitHub token and repository details
    token = os.getenv('GITHUB_TOKEN')
    repo_owner = 'Sanmilee'
    repo_name = 'testy'


    repo = clone_repo(repo_url, clone_dir)
    create_branch(repo)
    create_readme(repo, readme_file, readme_content)
    commit_and_push(repo, repo.head.ref.name, 'Add README file with machine learning content')
    merge_branch(repo, repo.head.ref.name)


if __name__ == "__main__":
    main()
