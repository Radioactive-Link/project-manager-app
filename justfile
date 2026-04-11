drun := "uv run manage.py"

# run manage.py with uv
djr *ARGS:
    {{drun}} {{ ARGS }}

# start the django dev server
dev:
    {{drun}} runserver

# generate django migrations
makemigrations:
    {{drun}} makemigrations

# apply django migrations
migrate:
    {{drun}} migrate
