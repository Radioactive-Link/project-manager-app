drun := "uv run manage.py"

# run manage.py with uv
djr:
    {{drun}}

# start the django dev server
dev:
    {{drun}} runserver

# generate django migrations
makemigrations:
    {{drun}} makemigrations

# apply django migrations
migrate:
    {{drun}} migrate
