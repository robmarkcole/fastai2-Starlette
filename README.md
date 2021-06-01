# Starter for deploying [fast.ai](https://www.fast.ai) models with Starlette

This repo can be used as a starting point to deploy [fast.ai](https://github.com/fastai/fastai) models with Starlette.

See the Deployment notebook for hints

To run locally:
`python3 app/server.py`

## Dev
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip3 install -r requirements.txt`
* `pip3 install -r requirements-dev.txt`
* `venv/bin/jupyter lab` or `python3 app/server.py`