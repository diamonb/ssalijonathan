from exts import db

"""
Class Recipe:
    id : Integer
    title : String
    description :  String
"""
class Recipe(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    title = db.Column(db.String(), nullable = False)
    description =  db.Column(db.Text(), nullable = False)
    def __repr__(self):
        return f'Recipe {self.title}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, title, description):
        self.title=title
        self.description=description
        db.session.commit()
    def to_dict(self): 
        return { 
            "id": self.id,
            "title": self.title, 
            "description": self.description 
            }

"""
Class User:
    id : Integer
    username : String
    email :  String
    password : String
"""
class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(25), nullable = False, unique = True)
    email =  db.Column(db.String(80), nullable = False, unique = True)
    password =  db.Column(db.String(), nullable = False)
    def __repr__(self):
        return f'User {self.title}'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self, username):
        self.username=username
        db.session.commit()
    def to_dict(self): 
        return { 
            "id": self.id,
            "username": self.username, 
            "email": self.email,
            'password': self.password
            }