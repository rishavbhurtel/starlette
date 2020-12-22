import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

def info(request):
    if request.path_params:
        user_id = request.path_params['user_id']
        if user_id == 1:
            #return JSONResponse({'Name': "Rishav", "Id": user_id, "Address": "Kathmandu"})
            return templates.TemplateResponse('info.html',{'request':request,
                                                            'Name': "Rishav",
                                                            "Id": user_id,
                                                            "Address": "Kathmandu"})
        else:
            return templates.TemplateResponse( 'info.html',{'request':request,
                                                            'Name': "Unknown",
                                                            "Id": user_id,
                                                            "Address": "Unknown"})
    else:
        return PlainTextResponse("No parameter. Please Enter Id number")

routes = [  
    Route('/', homepage),
    Route('/info/{user_id:int}', endpoint=info),
    Route("/info", endpoint=info)
]

app = Starlette(debug=True, routes=routes, reload=True)
app.mount('/static', StaticFiles(directory='statics'), name='static')
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
