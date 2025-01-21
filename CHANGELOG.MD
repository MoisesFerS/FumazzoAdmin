# CHANGELOG

All of the changes of the project will be listed here.

The format is based on:

[Keep a Changelog](https://keepachangelog.com/)
[Semantic Versioning](https://semver.org/)

## [0.1.0] - 20/01/2025 -  Project Initialization

### ADDED

- Created the files:
    - `.gitignore` - To keep unwanted files away from the repository.
    - `CHANGELOG.MD` - To keep track of the changes on the project.
    - `requirements.txt` - The file that contains the dependecies to the project.

- Set up the basic Django project structure.

### CHANGED

- Updated `FumazzoAdmin/settings.py` with the following configurations:
    - Moved database connection details to the `.env` file for security.
    - Configured the path to the templates folder.
    - Adjusted paths for static and media files.
    - Moved the Django secret key to the `.env` file.
    - Updated timezone and language settings.
    - Configured the default phone region.