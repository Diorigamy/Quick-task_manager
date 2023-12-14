
linux bash commands:
clone the repository 
cd /into/repositoryfolder
sudo  apt-get install python3
sudo apt-get install nginx  "and configure your site available and enabled or symbolically link, nginx will work with gunicorn"
python3 -m venv venv "install enviroment for the app to run"
source venv/bin/activate "activate the enviroment"
pip install -r envinstall.txt "installing the relevant enviroment and dependecies"
activate sqlalachemy Flask-sqlachemy as well as sqlite 3 among other env
ensure nginx is running ,bind gunicorn to nginx an start the app(feel free to run my custom 'reload' bash script initializes on http://localhost:8000)
if you encounter any database issues , run python3 , and initialize db with "Flask init-db" then "init_db()"
FEEL FREE TO IMPROVE, ADD AND UPDATE ANY CONTENT

The program is a Flask web application for managing tasks.
 Let's break down the key components and explain the technologies, structure, and flow of the program:
Technologies Employed:
Flask:
Flask is a micro web framework for Python.
It's used to build web applications quickly and with minimal code.
Handles routing, templates, and other web-related tasks.
SQLAlchemy:
SQLAlchemy is used for database management within Flask applications.
It provides a high-level ORM (Object-Relational Mapping) for interacting with the SQLite database.
SQLite:
SQLite is a lightweight, file-based relational database management system.
It's used for storing user and task data in this application.
Jinja2:
Jinja2 is a template engine for Python.
It's used in Flask for rendering HTML templates.
Werkzeug:
Werkzeug is a utility library for WSGI (Web Server Gateway Interface) applications.
Included in Flask for handling various tasks like password hashing.
Bootstrap:
Bootstrap is a popular front-end framework for building responsive and visually appealing web pages.
Used for styling the HTML templates.
jQuery and Flatpickr:
jQuery is a JavaScript library simplifying HTML document traversal and manipulation.
Flatpickr is a lightweight and powerful datetime picker library.
Used for handling date and time input in the create task form.
Structure of the Program:
Database Setup (schema.sql):
Defines the structure of two tables, users and tasks, in an SQLite database.
Users table stores user information, and tasks table stores task-related data.

Flask Application (app.py):
Defines a Flask application and sets up configurations.
Uses SQLAlchemy for database connections and ORM.
Defines two classes, User and Task, as models for database tables.
Routes and Views (app.py):
Defines routes for registration, login, logout, task creation, editing, and deletion.
Implements views for rendering HTML templates and handling user interactions.
HTML Templates (templates folder):
Uses Jinja2 templating engine for dynamic content rendering.
Templates include base.html, create_task.html, index.html, register.html, login.html, and view_task.html.
CSS Styles (static/styles.css):
Provides styling for the HTML templates using CSS.
Enhances the visual appeal and user experience of the web application.



Flow and How It Works:
Initialization (app.py):
Initializes the Flask app, SQLAlchemy, and login manager.
Defines models for user and task with corresponding database tables.
Database Initialization (app.py):
Uses schema.sql to create and initialize the SQLite database.
User Authentication (app.py):
Implements user registration, login, and logout functionalities.
Uses password hashing for security.
Task Management (app.py):
Defines routes and views for creating, editing, deleting, and viewing tasks.
Tasks are associated with users through the user_id foreign key.
Templates and Styling (templates and static/styles.css):
HTML templates define the structure and layout of web pages.
CSS styles enhance the visual presentation of the application.

Datetime Picker (create_task.html):
Utilizes Flatpickr for providing a user-friendly date and time input in the create task form.
Navigation (base.html):
Provides a navigation bar with links to home, login, register, and logout pages.
Dynamic Content Rendering (Jinja2):
Uses Jinja2 templating to render dynamic content in HTML templates.
User Sessions (Flask Session):
Manages user sessions to keep track of logged-in users.
Error Handling and Flash Messages (app.py):
Handles errors and displays flash messages for user feedback.
In summary, the application employs Flask and related technologies to create a task management web application with user authentication, database storage, and dynamic HTML templates. Users can register, log in, create, edit, and delete task

