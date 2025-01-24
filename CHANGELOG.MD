# CHANGELOG

All of the changes of the project will be listed here.

The format is based on:

[Keep a Changelog](https://keepachangelog.com/)
[Semantic Versioning](https://semver.org/)

## [0.7.0] - 23/01/2025 - Adding Simple Forms

### ADDED
- Created the following forms in `forms/core/`:
    - `category` - Form to register categories for `products`, `meals`, and `drinks`.
    - `meal` - Form to register a new meal.
    - `product` - Form to register a product.
    - `restock` - Form to register stock entries.
    - `supplier` - Form to register a supplier.
- Created the following forms in `forms/workers/`:
    - `role` - Form to register roles for workers.
    - `shift` - Form to register shifts for workers.
    - `worker` - Form to register a worker.
- Added `template.html` in `forms/` as a base template for importing forms.
- Created directories:
    - `css/core/` - To store CSS files for the `core` app pages.
    - `css/workers/` - To store CSS files for the `workers` app pages.
- Added `login.css` in `css/workers/`.

### CHANGED
- Moved the `login.html` form from `forms/core/` to `forms/workers/`.
- Updated the `login` view in `workers/views.py` to support a dynamic form using `forms/template.html`.
- Updated the `login` form in `forms/workers/` and adjusted styles to use the new `login.css`.
- Replaced `logo.png` with a higher-resolution version.

### REMOVED
- Removed the `type` attribute from the `product` form, as `category` objects will now be used.

## [0.6.0] - 23/01/2025 - Adding Font and Enhancing Header

### ADDED
- Added `DMSans.ttf` font to `static/fonts`.

### CHANGED
- Updated `header.html` to display worker information.
- Enhanced the view logic to retrieve and display worker permissions.
- Updated `styles.css` to reflect adjustments made to `header.html`.
- Corrected typos in `CHANGELOG.MD`.

## [0.5.1] - 23/01/2025 - Fixing URLS

### CHANGED
- `URLs:`
    - Updated `Fumazzo/urls.py`:
        - Set the `authentication app` to `workers` by changing the primary path.
        - Set the `core app` as the manager by assigning it the secondary path.
- `Templates:`
    - Swapped templates between `templates/core/` and `templates/workers/` to align with their respective app responsibilities.
- `Views:`
    - Reorganized `views.py` files:
        - Adjusted views and paths to correspond to the correct app (`core` or `workers`).
- `Header Namespaces:`
    - Updated the `header` template namespaces:
        - Changed references from `core` to `workers`.

## [0.5.0] - 22/01/2025 - Views Paths

### ADDED
- Created `login` form at `partials/forms/`.
- Created `static/fonts/` folder and added the `Oswald.ttf` font.
- Added assets:
    - `logo.png` - Project logo.
    - `background.png` - Background image for pages.
    - Navbar icons.

### CHANGED
- Settings:
    - Updated `Fumazzo/settings.py` to include static file configurations.
- URLs:
    - Updated `Fumazzo/urls.py` to include:
    - `core/urls` - Routes requests to the correct views in the `core` app.
    - `workers/urls` - Routes requests to the correct views in the `workers` app.
    - `Updated urls.py` in both apps to include namespaces for better URL resolution.
- Core Views:
    - Added:
        - `index` - Renders the main page of the core app.
        - `login` - Renders the login page of the core app and authenticates workers.
        - `logout` - Logs out users by flushing their session.
- Workers Views:
    - Added:
        - `index` - Renders the main page of the `workers` app.
- Base Site Structure:
    - Updated templates:
        - `base.html` - Defines the basic structure of the site's HTML.
        - `header.html` - Site header.
        - `footer.html` - Site footer.
- Updated `styles.css` to refine the base page's styling.
    - Dependencies:
        - Added `bcrypt` to `requirements.txt` for secure password hashing.

## [0.4.0] - 22/01/2025 - Forms and Models

### ADDED
- Created the following models at `core.models`:
    - `Supplier` - Stores supplier data.
    - `Product` - Stores stock product data.
    - `Category` - Organizes meals and products.
    - `Restock` - Tracks products added to stock.
    - `Resupply` - Stores entries of product batches.
    - `ProductMeal` - Relation between Products (ingredients) and Meals.
- Created the following models at `workers.models`:
    - `Shift` - Stores worker shift data.
    - `Role` - Stores worker role data.
    - `Worker` - Stores worker data.
- Added the following forms at `core.forms`:
    - `SupplierRegister` - Form to register a supplier.
    - `ProductRegister` - Form to register a product in stock.
    - `CategoryRegister` - Form to register a new category.
    - `RestockRegister` - Form to register a stock entry.
    - `MealRegister` - Form to register a meal.
- Added the following forms at `workers.forms`:
    - `ShiftRegister` - Form to register a shift.
    - `RoleRegister` - Form to register a role.
    - `WorkerRegister` - Form to register a new worker.
- Created `products` and `meals` folders at `media/core/` for storing product and meal media files.
- Added `phonenumber_field` to `INSTALLED_APPS` in `FumazzoAdmin/settings.py` to enable phone number handling with Django.
- Added `setuptools` to `requirements.txt` for running the server on Linux.

### CHANGED
- Fixed typos in `CHANGELOG.MD`.

## [0.3.0] - 21/01/2025 - Folder Structure

### ADDED
- Created the following folder structure:
    - `static` - For static files related to page structure.
        - `css` - Stores all CSS files.
        - `icons` - Stores icons used in the project.
        - `images` - Stores images related to the pages.
        - `js` - Stores all JavaScript files used.
    - `templates` - For HTML templates.
        - `core` - Stores templates for the core app.
        - `partials` - Stores reusable pieces of HTML.
            - `forms` - Stores all forms.
        - `workers` - Stores templates for the workers app.
    - `media` - For uploaded files.
        - `core` - Stores uploads from the core app.
        - `workers` - Stores uploads from the workers app.
- Created the following files:
    - `base.html` - Base template at `templates/`.
    - Created `header.html` and `footer.html` - Partial templates stored at `templates/partials/` for reusable page sections.
    - `styles.css` - CSS file at `static/css/`.
    - `scripts.js` - JavaScript file at `static/js/`.
    - `index.html` - Created for both `templates/core` and `templates/workers`.
- Added `.gitkeep` files to empty folders to ensure they are tracked by Git.

 
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
- Updated `FumazzoAdmin/settings.py` to include both apps in the `INSTALLED_APPS` configuration.

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