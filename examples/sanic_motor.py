""" sanic motor (async driver for mongodb) example
Required packages:
pymongo==3.4.0
motor==1.1
sanic==0.2.0
"""
from sanic import Sanic
from sanic import response
from motor.motor_asyncio import AsyncIOMotorClient


app = Sanic('motor_mongodb')
MotorClient = None


def get_db():
    global MotorClient
    if not MotorClient:
        mongo_uri = "mongodb://127.0.0.1:27017/test"
        client = AsyncIOMotorClient(mongo_uri)
        MotorClient = client['test']
    return MotorClient


@app.route('/objects', methods=['GET'])
async def get(request):
    db = get_db()
    docs = await db.test_col.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return response.json(docs)


@app.route('/post', methods=['POST'])
async def new(request):
    doc = request.json
    print(doc)
    db = get_db()
    object_id = await db.test_col.save(doc)
    return response.json({'object_id': str(object_id)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
