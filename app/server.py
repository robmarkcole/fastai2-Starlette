# uvicorn imports
import aiohttp
import asyncio
import uvicorn

# starlette imports
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

# fastai
# from fastai.vision import *
# from fastai.imports import *
# from fastai import load_learner
from fastai.vision.all import *

# Any custom imports should be done here, for example:
# from lib.utilities import *
# lib.utilities contains custom functions used during training that pickle is expecting


# export_file_url = YOUR_GDRIVE_LINK_HERE
export_file_name = 'resnet18.pkl' # from https://www.dropbox.com/s/lya2a16ca27dpig/resnet18.pkl?raw=1

classes = ['Agrostemma-githago_Cotyledon', 'Agrostemma-githago_Foliage', 'Agrostemma-githago_Intermediate', 'Beta-vulgaris_Cotyledon', 'Beta-vulgaris_Foliage', 'Beta-vulgaris_Intermediate', 'Crepis-setosa_Cotyledon', 'Crepis-setosa_Foliage', 'Crepis-setosa_Intermediate']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    # await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path/export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
  img_data = await request.form()
  img_bytes = await (img_data['file'].read())
  img_np = np.array(Image.open(BytesIO(img_bytes)))
  pred = learn.predict(BytesIO(img_bytes))
  return JSONResponse({
      'result': str(pred[0])
  })


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
