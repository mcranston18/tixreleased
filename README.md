# Tix released

## Dependencies

pipenv (https://pypi.org/project/pipenv/)

## Set up

1. Install project dependencies
```
pipenv install
```

2. Duplicate `.sample.env` and rename to `.env`

3. Enter virtual environment
```
pipenv shell
```

4. Start project
```
./manage.py runserver
```

## Testing

```
pylint . # pass -s when using debugger
```

## Formatting

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

The highly opinionated Black formatting tool takes care of all formatting
