from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from model import Recipe
from exts import db
import json
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app,doc='/docs')
db.init_app(app)

migrate = Migrate(app,db)
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
    
@api.route('/recipe/<int:id>')
class RecipeRessource(Resource):
    @api.marshal_list_with(Recipe_model)
    def get(self,id):
        """"Get a recipe"""
        recipe = Recipe.query.get_or_404(id)
        return recipe
    @api.marshal_list_with(Recipe_model)    
    def put(self,id):
        """"Update a recipe"""        
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'),data.get('description'))
        return recipe_to_update
    
    @api.marshal_list_with(Recipe_model)    
    def delete(self,id):
        """"Delete a recipe"""        
        recipe_to_delete = Recipe.query.get_or_404(id)
        recipe_to_delete.delete()
        return recipe_to_delete
    
# @app.route('/reciperr/<int:id>')
# def getRecipe(id):
#     """"Get a recipe"""
#     recipe = Recipe.query.get_or_404(id)
#     return json.dumps(recipe.to_dict())
    
if __name__ == '__main__':
    app.run()