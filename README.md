## Project Description

The project aims to implement DeepONet & FNO for perplexity 3 of IMC @Web.

## Installation & Setup

### Dependencies
This project uses `uv` as a package manager. To add a new dependency, modify the `dependencies` section in `pyproject.toml`. To remove a library, simply delete the corresponding line from the same section.

### UV Package Manager
To install dependencies using `uv`:
~~~bash
uv pip install -e .  # Install the project in editable mode
~~~

### Usage

This project provides two launch scripts tailored for different environments: one for Unix-like systems and one for Windows.

#### On Unix (Linux/macOS)
Make the `launch.sh` script executable and run it:
~~~bash
chmod +x launch.sh  # Make the script executable
./launch.sh         # Run the script
~~~

#### On Windows
A dedicated PowerShell script `launch.ps1` is provided for Windows users (actually only on branch of arthur, since I am the only one that ran into the problem). Follow these steps:

1. Open PowerShell and navigate to the project directory:
   ~~~powershell
   cd C:\path\to\your\project
   ~~~
2. If necessary, adjust the execution policy to allow script execution:
   ~~~powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ~~~
3. Run the script:
   ~~~powershell
   .\launch.ps1
   ~~~

Both scripts perform the following operations:
- Install `uv` (if not already installed)
- Set the `UV_LINK_MODE` environment variable (initially to `symlink`)
- Create (or update) and activate a virtual environment via `uv`
- Change the link mode to `copysync` for the project installation
- Install the project in editable mode
- Clean the `uv` cache
- Run a test to verify that the environment is correctly configured

### Git Commands

To merge the `main` branch into all individual branches (janis, fouad, laurent, arthur) and push the changes, use the following command:
~~~bash
for branch in janis fouad laurent arthur; do git checkout $branch && git merge main && git push origin $branch; done
~~~

> **Note:**  
> When merging branches, ensure that the appropriate launch script is preserved for each environment. It is recommended to maintain both `launch.sh` and `launch.ps1` in the repository and document in this README which script to use based on your operating system.
