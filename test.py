from datetime import datetime
import uvicorn
from sqlalchemy import Table, select, create_engine, MetaData
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Info
from config import DB_PATH

Base = declarative_base()

engine = create_engine(DB_PATH)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()
templates = Jinja2Templates(directory='templates')

async def homepage(request):
    r_infos = s.query(Info).order_by(Info.id.asc()).all()
    s.close()
    return templates.TemplateResponse('index.html', {'request': request, 
                                                'date':(datetime.now()).strftime("%Y-%b-%d, %H:%M:%S"),
                                                'infos': r_infos})

async def info(request):
    if request.path_params:
        info_id = request.path_params['info_id']
        r_infos = s.query(Info).filter_by(id=info_id).first()
        #return JSONResponse({'Name': "Rishav", "Id": user_id, "Address": "Kathmandu"})
        return templates.TemplateResponse('info.html',{'request':request,
                                                        'infos': r_infos})
    else:
        return PlainTextResponse("No parameter. Please Enter Id number")

async def delete(request):
    if request.path_params:
        info_id = request.path_params['info_id']
        s.query(Info).filter_by(id=info_id).delete()
        s.commit()
        s.close()
        response = RedirectResponse(url='/', status_code=303)
        return response
    else:
        return PlainTextResponse("No parameter.")

async def add(request):
    if request.method == "POST":
        print("Add Request!")
        data = await request.json()
        id, name, address = data['id'], data['name'], data['address']
        s.add(Info(id = id, name = name, address = address))
        s.commit()
        s.close()
        return PlainTextResponse("Success")
    if request.method == "GET":
        return templates.TemplateResponse('add.html',{'request':request})

async def update(request):
    if request.path_params:
        if request.method == "POST":
            print("Updating!")
            id = request.path_params['info_id']
            data = await request.json()
            name, address = data['name'], data['address']
            s.query(Info).filter_by(id=id).update({"id":id, "name":name, "address":address})
            s.commit()
            s.close()
            return PlainTextResponse("Success")
            # response = RedirectResponse(url='/', status_code=303)
            # return response
        if request.method == "GET":
            info_id = request.path_params['info_id']
            info = s.query(Info).filter_by(id=info_id).first()
            return templates.TemplateResponse('update.html',{'request':request, 'info': info})
    else:
        return PlainTextResponse("No parameter.")

routes = [
    Route('/', homepage),
    Route('/info/{info_id:int}', endpoint=info),
    Route("/info", endpoint=info),
    Route("/add", endpoint=add, methods=["GET","POST"]),
    Route("/edit/{info_id:int}", endpoint=update, methods=["GET","POST"]),
    Route("/delete/{info_id:int}", endpoint=delete)
]   

app = Starlette(debug=True, routes=routes)
app.mount('/static', StaticFiles(directory='statics'), name='static')
if __name__ == "__main__":
    uvicorn.run('test:app', host='0.0.0.0', port=8000, reload=True)
