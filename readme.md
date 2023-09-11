# Standard Wear

## Description

Ecommerce website for a clothing of basic and customizable clothing.

## Project stack

- Python
- Django
- PostgreSQL
- Redis
- Celery

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run the server
5. Run redis server
6. Run celery worker

### Clone the repository

```bash
git clone
```

### Create a virtual environment

```bash
python -m venv venv
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
python manage.py runserver
```

### Run redis server

```bash
redis-server
```

### Run celery worker

```bash
celery -A standardwear worker -l info
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

```

```
