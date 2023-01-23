from flask import Flask 
from flask import render_template,request,redirect
import psycopg2
from flask import flash
from datetime import datetime
from random import randint
from database import abrirConexion,cerrarConexion
app= Flask(__name__)

conexion= abrirConexion()



@app.route('/')


def index():
   
    return render_template('index.html')

@app.route('/update',methods=['POST'])
def update():
    cur= conexion.cursor()
    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _edad=request.form['txtEdad']
    _cedula=request.form["txtCedula"]
    query="UPDATE  formulario SET nombre=%s,apellido=%s,edad=%s WHERE cedula=%s;"
    datos=(_nombre,_apellido,_edad,_cedula)
    cur.execute(query,datos)
    conexion.commit() 
    return redirect('/almacenados')



@app.route('/store', methods=['POST'])
def storage():
  try:
    _cedula=request.form["txtCedula"]
    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _edad=request.form['txtEdad']
    cur=conexion.cursor()  
   
    query="INSERT INTO formulario( cedula,nombre,apellido,edad) VALUES (%s,%s,%s,%s)"
    datos=(_cedula,_nombre,_apellido,_edad)
    
    cur.execute(query,datos)
    conexion.commit()
    return render_template('index.html')
  except ValueError:
     flash('esta ingresando datos erroneos')
     return redirect('index.html')




@app.route('/almacenados')
def almacenados():
    cur=conexion.cursor()
    query="SELECT * FROM formulario"
    cur.execute(query)
    formulario=cur.fetchall()
    print(formulario)
    conexion.commit()
    return render_template('almacenados.html',formulario=formulario)





@app.route('/destroy/<int:cedula>')
def destroy(cedula):
    cur=conexion.cursor()  
    cur.execute("DELETE FROM formulario WHERE cedula=%s",[cedula])
    conexion.commit()
    return redirect('/almacenados')


@app.route('/edit/<int:cedula>')
def edit(cedula): 
    cur=conexion.cursor()
    cur.execute("SELECT * FROM formulario WHERE cedula=%s",[cedula])
    formulario=cur.fetchall()
    conexion.commit()
    return render_template('edit.html',formulario=formulario)

@app.route('/formularios_guardados')
def formularios_guardados():
    return render_template('formularios_guardados.html')

if __name__ == '__main__':
    app.run(debug=True)

def cerrarConexion():
    conexion.close()