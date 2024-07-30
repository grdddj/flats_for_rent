# Flats for rent

Finding the current state of flats for rent in a certain development project.

## Working

Fetchess all the flats as HTML pages, parses them and saves them in a JSON file. Also, reports any differences between current state and the previous state.

## Usage

```sh
python get_flats.py
```

## Prerequisites

- Creating `config.json` file with a `Pushbullet` token - see `config.mock.json` for the required structure
