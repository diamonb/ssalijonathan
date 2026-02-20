from flask import Flask,request
from flask_restx import Api,Resource,fields
from config import DevConfig
from model import Recipe
from exts import db



app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app,doc='/docs')
db.init_app(app)

#model serialize
Recipe_model = api.model("Recipe",
                         {
                             "id": fields.Integer,
                             "title": fields.String,
                             "description": fields.String
                         })
@api.route('/accueil')
class HelloRessource(Resource):
    def get(self):
        return "<p>Accueil</p>"
    
@api.route('/recipes')
class RecipesRessource(Resource):
    @api.marshal_list_with(Recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return recipes
    
    @api.marshal_list_with(Recipe_model)
    def post(self):
        """ Post recipe """

        data = request.get_json()
        new_recipe = Recipe(
            title = data.get('title'),
            description = data.get('description')
        )
        new_recipe.save()
        return new_recipe,201
    
@api.route('/recipe/{<int:id>}')
class RecipeRessource(Resource):
    def update(self,id):
        """ Get all recipes """
        pass
    def delete(self,id):
        """ Post recipe """
        pass


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Recipe': Recipe
    }

    
if __name__ == '__main__':
    app.run()