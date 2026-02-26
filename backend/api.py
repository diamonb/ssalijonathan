from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from model import Recipe,User
from exts import db
import json
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash



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

Sign_up_model = api.model("Sign_up",
                         {
                             "username": fields.String,
                             "email": fields.String,
                             "password" :fields.String
                         })

@api.route('/accueil')
class HelloRessource(Resource):
    def get(self):
        return "<p>Accueil</p>"
    
@api.route('/signup')
class SignupRessource(Resource):
    @api.marshal_list_with(Sign_up_model)
    def get(self):
        users = User.query.all()
        return users
    @api.marshal_with(Sign_up_model)
    @api.expect(Sign_up_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        db_user = User.query.filter(User.username==username).first()
        if db_user :
            return jsonify({'message':f'Utilisateur {username} existe déjà'})
        new_user = User(
            username = username,
            email = email,
            password = generate_password_hash(password)
        )
        new_user.save()
        return new_user
    
@api.route('/login')
class LoginRessource(Resource):
    pass
    
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
    
    @api.marshal_with(Recipe_model)
    @api.expect(Recipe_model)
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
    @api.marshal_with(Recipe_model)
    def get(self,id):
        """"Get a recipe"""
        recipe = Recipe.query.get_or_404(id)
        return recipe
    @api.marshal_with(Recipe_model)    
    def put(self,id):
        """"Update a recipe"""        
        recipe_to_update = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe_to_update.update(data.get('title'),data.get('description'))
        return recipe_to_update
    
    @api.marshal_with(Recipe_model)    
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