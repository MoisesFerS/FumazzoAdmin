# CHANGELOG

All of the changes of the project will be listed here.

The format is based on:

[Keep a Changelog](https://keepachangelog.com/)
[Semantic Versioning](https://semver.org/)

## [0.12.0] - 14/03/2025 - Products and Categories

### ADDED
- Addedd at `templates/core/`:
    - `categories.html` -
    - `products.html` - 
- Added at `static/js/`:
    - `categories.js` -
    - `products.js` - 
- Added at `static/css/`:
    - `categories.css` -
    - `products.css` - 
- Added new routes in `core/urls.py` for new defs in `core/views.py`:
    - `categories` - Render categories template.
    - `products` - Render products template.
<!-- - Added to `Stock System` the function to register a new supplier. -->

### CHANGED
- Renamed the field `individual_price` to `sell_price` in the `Products` model.

### REMOVED
- `partials/forms/*` - Was deprecated.

## [0.11.0] - 14/03/2025 - Meal System Integration

### ADDED
- Added `meal.html`: the HTML template for the meal system page.
- Added `meal.css`: styles for the meal management page.
- Added `meal.js`: JavaScript for meal-related dynamic interactions.
- Added Navbar Link to the meal system in the main navigation bar.
- Added new routes in `core/urls.py` for new defs in `core/views.py`:
  - `meal`: Renders the meal management page.
  - `get_categories`: Retrieves categories when selecting a type in the "meal add" modal.
  - `meal_add`: Registers a new meal entry.
  - `meal_data`: Retrieves meal information for editing.
  - `meal_edit`: Updates the meal information.
  - `meal_remove`: Removes a meal entry.
  - Ingredient Operations: Added routes to manage meal ingredients:
    - `ingredient_add`: Adds an ingredient to a meal.
    - `ingredient_increment`: Increases the quantity of a selected ingredient.
    - `ingredient_subtract`: Decreases the quantity of a selected ingredient.
    - `ingredient_remove`: Removes an ingredient from a meal.

### CHANGED
- Model Update: Renamed the `meal_product` model to `Ingredient` for clearer representation in the context of meals.

## [0.10.0] - 27/02/2025 - Developing the index's Pages

### ADDED
- Added the `favicon.ico`.
- Added the `error messages modal`, which displays errors on the screen for three seconds, or until the user clicks to dismiss it.
- Added content to:
    - `worker/index.html`.
    - `core/index.html`.
- Added `index.css` to `css/workers/` (dashboard).
- Added `index.js` to `js/workers/` (dashboard).
- Added `index.css` to `css/core/` (management).
- Added the defs to `workers/views.py`:
    - `index` - Renders the dashboard with worker data.
    - `get_shift` - Gets the worker shift data.

### CHANGED
- Updated the context to pass complete worker objects instead of individual attributes.
- Updated the authentication function in `worker/views.py`.
- Changed the default scrollbar to a custom style for a more consistent design.

## [0.9.0] - 24/02/2025 - Adding the Stock System

### ADDED
- Added the `NAME_PATTERNS.md` file.
- Added the storage page link to `storage button` at navbar.
- Added the `Stock System`:
    - Add `stock` entries.
    - Edit `stock` entries.
    - Add `products` to `stock` entries.
    - Remove `products` from `stock` entries. 
    - Remove `stock` entries.
- Added to `styles.css`:
    - Color variable `detail 4` - Green.
    - Color variable `detail 5` - Mustard.
    - Color variable `detail 6` - Red.
    - `button-secondary` - Green background.
- Added the defs at `core/views.py`:
    - `stock` - Render the stock page.
    - `get_products` - Get every product by its category.
    - `stock_add` - Add a stock entry.
    - `load_product` - Loads the products in a stock.
    - `stock_edit_save` - Saves the edition and products added/removed from stock.
    - `stock_remove` - Removes a  stock entry.
- Added the icons at `static/icons/`:
    - `edit.ico`
    - `trash-can.ico`
- Created the templates at templates/core/:
    - `stock.html`.
- Created the css at `css/core/`:
    - `stock.css`.
- Created the js at `js/core/`:
    - `stock.js`.
- Added the corresponding paths in `core/urls.py` for the new defs in `core/views.py`.

### CHANGED
- Adjusted all defs:
    - Corrected the usage of the `render` function to properly pass the `context`.
    - Added a underscore after all local variables.
- Changed the variables colors ids at `css/styles.css`.
- Renamed the `models`:
    - `Restock` to `Stock`.
    - `Ressupply` to `Supply`

### REMOVED
- Removed the attribute `expiration_date` from `Stock`.

## [0.8.1] - 25/01/2025 - Fixing Login Template

### ADDED
- Added a field and input type to the `Category` model, `forms.py`, and the corresponding form template.

### CHANGED
- Updated the login button in the header:
    - It no longer appears on the login page.
    - It now changes to a log-out button when a user is in session.
- Updated `styles.css` to include the `main` tag for better structure and styling.
- Modified templates to include a `div` with the `content` class for organizing page layout.
- Updated the CSS for radial inputs to improve their appearance.


## [0.8.0] - 24/01/2025 - Defs to Forms

### ADDED
- Added the following views in `core/views.py`:
    - `supplier` - To render the form to register a supplier.
    - `meal` - To render the form to register a meal.
    - `product` - To render the form to register a product.
    - `category` - To render the form to register a category.
- Added the corresponding paths in `core/urls.py` for the new views.
- Added a method to return the `name` of models that include a `name` field (applied to various models).

### CHANGED
- Updated all forms in `partials/forms/` to correct button functionality.
- Fixed the `meal` and `product` models in `core/models.py` to correctly handle the upload path.
- Updated the `MealRegister` and `ProductRegister` forms to include the `category` field.

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