# Starter for deploying [fast.ai](https://www.fast.ai) models with Starlette

This repo can be used as a starting point to deploy [fast.ai](https://github.com/fastai/fastai) models with Starlette.

See the Deployment notebook for hints

## Docker
```
docker build -t fastai-starlette-demo .
docker run -p 5000:5000 fastai-starlette-demo:latest
```

## Dev
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip3 install -r requirements.txt`
* `pip3 install -r requirements-dev.txt`
* `venv/bin/jupyter lab` or `venv/bin/python3 app/server.py`

## Issues
- `ModuleNotFoundError: No module named 'fastai2'` why?? Possible [dependency conflict](https://forums.fast.ai/t/deployment-platform-render/33953/553) Solution? Never use fastai in production