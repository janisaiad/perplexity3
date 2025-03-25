## Project Description

The project aims to implement DeepONet & FNO for perplexity 3 of IMC @Web.

## Installation & Setup

### Dependencies
This project uses `uv` as a package manager. To add a new dependency, modify the `dependencies` section in `pyproject.toml`. To remove a library, simply delete the corresponding line from the same section.

### UV Package Manager
To install dependencies using `uv`:
```bash
uv pip install -e .  # Install the project in editable mode
```

### Usage

To make the `launch.sh` script executable and run it:
```bash
chmod +x launch.sh  # Make the script executable
./launch.sh        # Run the script
```

### Git Commands
To merge main branch into all other branches and push them:
```bash
for branch in janis fouad laurent arthur; do git checkout $branch && git merge main && git push origin $branch; done
```
