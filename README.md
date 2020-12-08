# GPT-2 Webeditor

This is a simple Webeditor for completing text using GPT-2. It uses the [Bottle Web Framework](https://bottlepy.org/), [Brython](https://brython.info/) and [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple).

**Note:** This project is intended for use with models trained using gpt-2-simple, it is unknown whether it will work with models trained using other models as well.

## Features

- Simple WebUI for gpt-2-simple text generation
- Markdown live preview.

## Requirements

- All packages listed in `requirements.txt`
- python3 (likely 3.7, newer may not work)
- tensorflow < 2.0

## Usage

Use `python3.7 webeditor.py --help` to view a help message.

Full usage (may be outdated):

```
usage: webeditor.py [-h] [-p PORT] [-i INTERFACE] [--run-name RUNNAME]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to serve on
  -i INTERFACE, --interface INTERFACE
                        interface to serve on
  --run-name RUNNAME    run name of the finetuned model.
```

Then visit the address (`https://localhost:8080` by default).

Input some text and then **press tab** to complete the text. This may take some time.
