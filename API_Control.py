from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from concurrent.futures import ProcessPollExecutor as Process
from multiprocessing import Process
import uvicorn
import time


app = FastAPI()
app.mount("/static", StaticFiles(directory=r"C:\AutoRClone\LIB\API\static"), name="static")
templates = Jinja2Templates(directory=r"C:\AutoRClone\LIB\API\templates")


def ler_log():
    linhas_do_log = list()
    with open(r'C:\AutoRClone\LOG\LogDoPython.log', encoding="utf-8") as log:
        full_log = log.readlines()
        linhas_do_log = full_log[-40:]
        retorno = list(reversed(linhas_do_log))
    return retorno


@app.get('/', response_class=HTMLResponse)
async def view_log(request: Request) -> 'html':
    titles = ("LOG")
    linhas_do_log = ler_log()
    return templates.TemplateResponse('log.html', {'request': request,
                                                   'the_title': 'Log do aplicativo RClone',
                                                   'row_title': titles,
                                                   'log_row': linhas_do_log})


if __name__ == '__main__':
    # alvo = uvicorn.run('API_Control:app', host='0.0.0.0', port=80, log_level='info')
    proc = Process(target=uvicorn.run,
                   kwargs={
                       "app": "API_Control:app",
                       "host": "0.0.0.0",
                       "port": 80,
                       "log_level": "info"
                   })
    proc.daemon = True
    proc.start()
    print(proc)
    print(f'*********************************NOME: {__name__}')
    time.sleep(15)
