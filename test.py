import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from datetime import datetime
from db_test import get_db
from models import Info
from sqlalchemy import Table, select

templates = Jinja2Templates(directory='templates')

def get_items(table_name, item_type, limit=20):
    db, metadata = get_db()
    table = Table(table_name, metadata, autoload=True, autoload_with=db)
    sql = select([table])
    items = [item_type(item) for item in db.execute(sql).fetchmany(limit)]
    return items

def get_item(table_name, item_type, item_id):
    db, metadata = get_db()
    infos_table = Table(table_name, metadata, autoload=True, autoload_with=db)
    sql = select([infos_table]).where(infos_table.c.id == item_id)

    info = item_type(db.execute(sql).fetchone())

    if info:
        return info

    raise Exception('Info not found.')

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

app = Starlette(debug=True, routes=routes)
app.mount('/static', StaticFiles(directory='statics'), name='static')
if __name__ == "__main__":
    uvicorn.run('test:app', host='0.0.0.0', port=8000, reload=True)
