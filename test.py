import uvicorn
from starlette.applications import Starlette
from starlette.responses import Response, PlainTextResponse, RedirectResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from datetime import datetime
from db_test import get_db
from models import Info
from sqlalchemy import Table, select

templates = Jinja2Templates(directory='templates')

def get_items(table_name, item_type, limit=10):
    db, metadata = get_db()
    table = Table(table_name, metadata, autoload=True, autoload_with=db)
    sql = select([table])
    items = [item_type(item) for item in db.execute(sql).fetchmany(limit)]
    return items

# def get_item(table_name, item_type, item_id):
#     db, metadata = get_db()
#     infos_table = Table(table_name, metadata, autoload=True, autoload_with=db)
#     sql = select([infos_table]).where(infos_table.c.id == item_id)

#     info = item_type(db.execute(sql).fetchone())

#     if info:
#         return info

#     raise Exception('Info not found.')

def get_info(info_id):
    db, metadata = get_db()
    infos_table = Table('infos', metadata, autoload=True, autoload_with=db)
    sql = select([infos_table]).where(infos_table.c.id == info_id)

    info = db.execute(sql).fetchone()

    if info:
        return info

    raise Exception('Info not found.')

async def homepage(request):
    r_infos = [info.to_dict() for info in get_items('infos', Info, 10)]
    return templates.TemplateResponse('index.html', {'request': request, 
                                                'date':(datetime.now()).strftime("%Y-%b-%d, %H:%M:%S"),
                                                'infos': r_infos})



async def info(request):
    if request.path_params:
        info_id = request.path_params['info_id']
        r_infos = get_info(info_id)
        #return JSONResponse({'Name': "Rishav", "Id": user_id, "Address": "Kathmandu"})
        return templates.TemplateResponse('info.html',{'request':request,
                                                        'infos': r_infos})
    else:
        return PlainTextResponse("No parameter. Please Enter Id number")


async def delete_info(request):
    if request.path_params:
        info_id = request.path_params['info_id']
        db, metadata = get_db()
        infos_table = Table('infos', metadata, autoload=True, autoload_with=db)
        sql = infos_table.delete().where(infos_table.c.id == info_id)
        db.execute(sql)
        response = RedirectResponse(url='/')
        return response

    else:
        return PlainTextResponse("No parameter.")

async def add(request):
    if request.method == "POST":
        print("Add Request!")
        data = await request.json()
        id = data['id']
        name = data['name']
        address = data['address']
        db, metadata = get_db()
        infos_table = Table('infos', metadata, autoload=True, autoload_with=db)
        sql = infos_table.insert().values(id = id, name = name, address = address)
        db.execute(sql)
        response = RedirectResponse(url='/', status_code=307)
        return response
    if request.method == "GET":
        return templates.TemplateResponse('add.html',{'request':request})

async def update(request):
    if request.method == "POST":
        print("Updating!")
        id = request.path_params['info_id']
        data = await request.json()
        name = data['name']
        address = data['address']
        db, metadata = get_db()
        infos_table = Table('infos', metadata, autoload=True, autoload_with=db)
        sql = infos_table.update().where(infos_table.c.id==id).values(name = name, address = address)
        db.execute(sql)
        response = RedirectResponse(url='/')
        return response 
    if request.method == "GET":
        info_id = request.path_params['info_id']
        info = get_info(info_id)
        return templates.TemplateResponse('update.html',{'request':request, 'info': info})
    

routes = [  
    Route('/', homepage),
    Route('/info/{info_id:int}', endpoint=info),
    Route("/info", endpoint=info),
    Route("/add", endpoint=add, methods=["GET","POST"]),
    Route("/edit/{info_id:int}", endpoint=update, methods=["GET","POST"]),
    Route("/delete/{info_id:int}", endpoint=delete_info)
]   

app = Starlette(debug=True, routes=routes)
app.mount('/static', StaticFiles(directory='statics'), name='static')
if __name__ == "__main__":
    uvicorn.run('test:app', host='0.0.0.0', port=8000, reload=True)
