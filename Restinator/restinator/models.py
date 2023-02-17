# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from .views import app

# with app.app_context():
#     db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONs']=False

# class Todo(db.Model):
#     id=db.Column(db.Integer(), primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer,default=0)
#     date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
#     def __repr__(self):
#         return '<Task %r>'%self.id
    
# # class evals_maps(db.Model):
# #     id=db.Column(db.Integer(), primary_key=True)
# #     content = db.Column(db.String(200), nullable=False)
# #     completed = db.Column(db.Integer,default=0)
# #     date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
# #     def __repr__(self):
# #         return '<eval %r>'%self.id
    
    
