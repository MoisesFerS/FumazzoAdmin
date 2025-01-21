# CHANGELOG

All of the changes of the project will be listed here.

The format is based on:

[Keep a Changelog](https://keepachangelog.com/)
[Semantic Versioning](https://semver.org/)

## [0.2.0] - 21/01/2025 - Creating Apps

### ADDED

- Created a folder `apps` to organize the project’s apps.
- Created new apps:
    - `worker` - Responsible for managing the workers of Fumazzo.
    - `core` - Handles database registrations, alterations, and deletions.
- In both apps, created:
    - `urls.py` - Configures the view paths for each app.
    - `forms.py` - Stores forms used throughout the project.

### CHANGED

- Updated the `apps.py` in both apps to use the format `apps.<appname>` instead of `<appname>`, ensuring the correct import path.
- Updated `Fumazzo/settings.py` to include both apps in the `INSTALLED_APPS` configuration.



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