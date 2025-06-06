# Django Starter Template

A basic Django project template to kickstart your web development projects.

## Features

- Basic Django project structure
- Pre-configured settings
- Ready-to-use development environment

## Getting Started

1. Clone this repository
2. Create a virtual environment:
    ```
    python -m venv venv
    ```
3. Activate the virtual environment:
    - Windows: `venv\Scripts\activate`
    - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Run migrations:
    ```
    python manage.py migrate
    ```
6. Start the development server:
    ```
    python manage.py runserver
    ```

## Project Structure

```
django_starter/
├── manage.py
├── requirements.txt
└── core/
     ├── __init__.py
     ├── settings.py
     ├── urls.py
     └── wsgi.py
```

## License

This project is licensed under the MIT License.