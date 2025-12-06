from flask import Flask, render_template, request
from flask import make_response, jsonify
import json, math
import forms

app= Flask(__name__)
@app.route('/')
def home():
    return "Hello world"

@app.route('/index')
def index():
    titulo="IEVN1001"
    listado=["Python","Flask","HTML","CSS","Javascript"]
    return render_template('index.html', titulo=titulo, listado=listado)


@app.route('/aporb')
def aporb():
    return render_template('aporb.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    n1= request.form.get("a")
    n2= request.form.get("b")
    return "La multiplicacion de {} y {} es {}".format(n1,n2,int(n1)*int(n2))


@app.route("/distancia",methods=['GET','POST'])
def distancia(): 
    resultado1=0.0 
    resultado=0.0 
    distancia_clas=forms.DForm(request.form)
    if request.method=='POST' and distancia_clas.validate: 
        x1=distancia_clas.equis1.data
        y1=distancia_clas.igriega1.data
        x2=distancia_clas.equis2.data
        y2=distancia_clas.igriega2.data
        resultado1=math.sqrt(((float(x2)-float(x1))**2)+((float(y2)-float(y1))**2)) 
        resultado="La distacia es de {}".format(resultado1)
    return render_template('distancia.html', form=distancia_clas, resultado=resultado)
    

@app.route("/figuras", methods=['GET', 'POST'])
def figuras():
    resultado = ""
    
    if request.method == 'POST':
        figura = request.form.get("figura")
        valor1 = request.form.get("valor1")
        valor2 = request.form.get("valor2")

        try:
            if figura == "cuadrado":
                lado = float(valor1)
                area = lado ** 2
                resultado = "El área del cuadrado es {:.2f}".format(area)

            elif figura == "triangulo":
                base = float(valor1)
                altura = float(valor2)
                area = (base * altura) / 2
                resultado = "El área del triángulo es {:.2f}".format(area)

            elif figura == "circulo":
                radio = float(valor1)
                area = math.pi * (radio ** 2)
                resultado = "El área del círculo es {:.2f}".format(area)

            elif figura == "pentagono":
                lado = float(valor1)
                perimetro = 5 * lado
                apotema = lado / (2 * math.tan(math.pi / 5))
                area = (perimetro * apotema) / 2
                resultado = "El área del pentágono es {:.2f}".format(area)

            else:
                resultado = "⚠️ Selecciona una figura válida."
        except:
            resultado = "⚠️ Error: verifica los datos ingresados."

    return render_template('figuras.html', resultado=resultado)

@app.route("/hola")
def func():
    return "<h1>Holaaaa</h1>"

@app.route("/alumnos", methods=['GET', 'POST'])
def alumnos():
    mat=0
    nom=''
    apell=''
    email=''
    estudiantes=[]
    datos={}
    alumno_clas=forms.UserForm(request.form)
    if request.method=='POST' and alumno_clas.validate():
        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')

        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        apell=alumno_clas.apellido.data
        email=alumno_clas.email.data
        datos={'matricula':mat, 'nombre':nom.rstrip(), 'apellido':apell.rstrip(), 'email':email.rstrip()}

        data_str=request.cookies.get("usuario")
        if not data_str:
            return "No hay cookie guardada", 404
        
        estudiantes = json.loads(data_str)

        estudiantes.append(datos)
    response=make_response(render_template('Alumnos.html', form=alumno_clas, mat=mat, nom=nom, apell=apell, email=email))

    if request.method!='GET':
        response.set_cookie('usuario', json.dumps(estudiantes))

    return response
    
@app.route("/get_cookie")
def get_cookie():
        data_str=request.cookies.get("usuario")
        if not data_str:
            return "No hay cookie guardada", 404
        
        estudiantes = json.loads(data_str)
        return jsonify(estudiantes)

 
@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    form = forms.PizzaForm(request.form)
    pizzas = []
    total = 0

    data_str = request.cookies.get('pedido')
    if data_str:
        pizzas = json.loads(data_str)

    if request.method == 'POST' and form.validate():
        if request.form.get("accion") == "agregar":
            tamaño = form.tamanio.data
            ingredientes = form.ingredientes.data
            cantidad = form.cantidad.data

            precio_base = {"Chica": 50, "Mediana": 70, "Grande": 90}
            subtotal = precio_base[tamaño] * cantidad + len(ingredientes) * 10 * cantidad

            pizzas.append({
                "tamaño": tamaño,
                "ingredientes": ingredientes,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

        elif request.form.get("accion") == "quitar":
            index = int(request.form.get("indice"))
            if 0 <= index < len(pizzas):
                pizzas.pop(index)

        elif request.form.get("accion") == "terminar":
            total = sum(p["subtotal"] for p in pizzas)
            cliente = {
                "nombre": form.nombre.data,
                "direccion": form.direccion.data,
                "telefono": form.telefono.data,
                "total": total,
                "pizzas": pizzas
            }

            ventas_str = request.cookies.get("cookie_ventas")
            ventas = json.loads(ventas_str) if ventas_str else []
            ventas.append(cliente)

            total_general = sum(v["total"] for v in ventas)

            response = make_response(render_template(
                "pizzeria.html",
                form=form,
                pizzas=[],
                total=total,
                ventas=ventas,
                total_general=total_general,
                mensaje="Día terminado. Aquí están las ventas registradas."
            ))
            response.set_cookie("cookie_ventas", json.dumps(ventas))
            response.delete_cookie("pedido")
            return response

    response = make_response(render_template("pizzeria.html", form=form, pizzas=pizzas, total=total))
    response.set_cookie("pedido", json.dumps(pizzas))
    return response

@app.route('/ventas')
def ventas():
    ventas_str = request.cookies.get("cookie_ventas")
    if not ventas_str:
        return "No hay ventas registradas aún"
    ventas = json.loads(ventas_str)
    return jsonify(ventas)


@app.route("/user/<string:user>")
def user(user):
    return "<h1>Hasta la proximaaaaa{}</h1>".format(user)

@app.route("/square/<int:num>")
def square(num):
    return "<h1>The square of {} is {}</h1>".format(num, num*2)

@app.route("/repeat/<string:text>/<int:times>")
def repeat(text, times):
    return "<h1>"+" ".join([text]*times)+"</h1>"

@app.route("/suma/<float:a>/<float:b>")
def suma(a,b):
    return "<h1>The sum of {} and {} is {}.</h1>".format(a,b,a+b)



if __name__=='__main__':
    app.run(debug=True)