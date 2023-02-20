import pandas as pd
import numpy as np
import os
from flask import *
from datetime import datetime
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from flask_sqlalchemy import SQLAlchemy
#from restinator.models import *
import psycopg2

conn = psycopg2.connect(database="restinator",
                        host="host.docker.internal" ,
                        user="postgres",
                        password="admin",
                        port="5432")
print(conn.encoding)
conn.set_client_encoding('UTF8')

app=Flask(__name__)
app.config.from_object('config')
n = 10

########################## GESTION DB
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs']=False

# 3 / : relatif, 4 / : absolu
with app.app_context():
    db = SQLAlchemy(app)

# !!!
#     """
# >>> from app import app,db
# >>> app.app_context().push()
# >>> db.create_all()

# utiliser ce code pour créer la DB dans le terminal : créer la db dans dossier 'instance'
#    """
# !!!
########################## Fonctions et objets
class Todo(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>'%self.id
    
# class evals_maps(db.Model):
#     id=db.Column(db.Integer(), primary_key=True)
#     content = db.Column(db.String(200), nullable=False)
#     completed = db.Column(db.Integer,default=0)
#     date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
#     def __repr__(self):
#        return '<eval %r>'%self.id
    
def get_iframe(arrondissement=None,note=None,shiny=False):
    avis = pd.read_csv('restinator/Data/clean_avis.csv',sep='|')
    avis = avis.astype({'Note': 'int32'})
    if note:
        if note!='0':
            avis=avis[avis['Note']>=int(note)]
    if arrondissement:        
        if arrondissement!='0':
            avis=avis[avis['CP']=="750{:02d}".format(int(arrondissement))]
            print("750{:02d}".format(int(arrondissement)))
    print(avis.shape,flush=True)
    loc=[48.866667,2.333333] # Paris
    w = "600px"
    h = "450px"

    m = folium.Map(location=loc, tiles="OpenStreetMap", zoom_start=12)
    m.get_root().width = w
    m.get_root().height = h
    for i in range(0,len(avis)):
        nom = avis.iloc[i]['Nom']
        note = avis.iloc[i]['Note']
        url = avis.iloc[i]['Url']
        loc = [avis.iloc[i]['Lat'],avis.iloc[i]['Lon']]
        html =f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h3> {nom} </h3>
            <h4>{note}/5 </h4>
            <a href='{url}' target="_blank">Visiter la page</a>
        </body>
        </html>
        """ 
        iframe_pop = folium.IFrame(html)
        popup = folium.Popup(iframe_pop,
                            min_width=200,
                            max_width=200,
                            min_height=500,
                            max_height=500)
        folium.Marker(location = loc,popup = popup).add_to(m)
    if shiny :
        return m
    else:
        iframe = m.get_root()._repr_html_()
        return iframe

########################### PAGES ##########################
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
########################## TO DO LIST
@app.route('/todo/',methods=['GET','POST'])
def todo():
    if request.method=='POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo/')
        except:
            return('Issue')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo/')
    except:
        return 'Fail deleting'

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method=='POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/todo/')
        except:
            return 'Fail to update'
    else:
        return render_template('update.html',task=task_to_update)
########################## FIN TO DO LIST

########################## PARTIE MAP
########################## MAP AVIS

@app.route('/map/',methods=['GET','POST'])
def map():
    return render_template('map.html',iframe=get_iframe())


@app.route('/map_shiny/',methods=['GET','POST'])
def map_shiny():
    # cur.execute('SELECT * FROM public.evals LIMIT 1;')
    # fetchone = cur.fetchone()
    # resp = {
    #     'map' : get_iframe(shiny=False),
    #     'line' : fetchone
    # }
    return Response(get_iframe(shiny=False))

@app.route('/update_map/',methods=['POST'])
def update_map():
    if request.method=='POST':
        min_rate = request.form['rating']
        arrondissement = request.form['arrondissement']
    return render_template('map.html',iframe=get_iframe(arrondissement,min_rate))

########################## MAP CONTROLES

@app.route('/evals_map/',methods=['GET','POST'])
def evals_map():
    inspections_clean= pd.read_csv('restinator/Data/inspections_clean.csv',sep='|')
    #inspections_clean = pd.read_sql('SELECT * FROM evals;', conn)
    cps=inspections_clean.code_postal.dropna().unique()
    evals = inspections_clean.evaluation.unique()
    loc=[48.866667,2.333333] # Paris
    w = "600px"
    h = "450px"

    m_insp = folium.Map(location=loc, tiles="OpenStreetMap", zoom_start=12)
    m_insp.get_root().width = w
    m_insp.get_root().height = h
    evals_cluster = MarkerCluster(name = "Evaluations").add_to(m_insp)
    for i in range(0,len(inspections_clean)):
        
        nom = inspections_clean.iloc[i]['nom']
        eval_etab = inspections_clean.iloc[i]['evaluation']
        loc = [inspections_clean.iloc[i]['lat'],inspections_clean.iloc[i]['lon']]
        html =f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h3> {nom} : {eval_etab} </h3>
            
        </body>
        </html>
        """
        iframe_pop = folium.IFrame(html)
        popup = folium.Popup(iframe_pop,
                            min_width=200,
                            max_width=200)

        folium.Marker(location = loc,popup = popup).add_to(
            folium.FeatureGroup(
                name = inspections_clean.iloc[i]['nom']).add_to(
                    evals_cluster))
    iframe = m_insp.get_root()._repr_html_()
    return render_template('evals_map.html',iframe=iframe,
                                                  cps=cps,
                                                  evals=evals
                                                  )

########################## FIN MAP

########################## ABOUT US

@app.route('/about_us/<int:n>',methods=['GET','POST'])
def about(n):
    cur = conn.cursor()
    cur.execute('SELECT * FROM evals LIMIT 10;')
    line = cur.fetchone()
    res = [line*n]
    return render_template('about_us.html',quant=res)

########################## FIN ABOUT US

########################## GRAPHIQUES

@app.route('/basic_graphs/',methods=['GET','POST'])
def draw_something():
    return render_template('basic_graphs.html')

########################## FIN GRAPHIQUES

if __name__=='__main__':
    app.run(debug=True)
    