from sanic import Sanic
from sanic.response import text,json
from DB.MongoHelp import MongoHelper as SqlHelper

class apiNews:
    def __init__(self):
        self.sqlhelper = SqlHelper()
        self.sqlhelper.init_db()

    def queryNews(self,category,pz,page):
        newsJson = self.sqlhelper.select(pz,{'category':category},page)
        return newsJson
        print (newsJson)

apiNews=apiNews()
app = Sanic(__name__)
@app.route("/news",methods=['GET'])
async def get_handler(request):
    parameter = request.args
    return json(apiNews.queryNews(parameter['category'][0],parameter['pageSize'][0],parameter['page'][0]))
app.run(host="0.0.0.0", port=8000, debug=True)