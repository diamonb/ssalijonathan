from flask import Flask
from flask_restx import Api,Resource
from config import DevConfig



app = Flask(__name__)
app.config.from_objet(DevConfig)
api = Api(app,doc='/docs')

@api.route('/accueil')
class HelloRssource(Resource):
    def get(self):
        return "<p>Accueil</p>"
    
if __name__ == '__main__':
    app.run()