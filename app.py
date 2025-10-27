from flask import Flask,render_template, request
import math

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World"


@app.route("/index")
def index():
    titulo="IEVN1001"
    listado=["Python","Flask","HTML","CSS","JavaScript"]
    return render_template('index.html', titulo=titulo, listado=listado)

@app.route("/aporb")
def aporb():
    return render_template('aporb.html')

@app.route("/resultado", methods=['POST'])
def resultado():
    n1 = request.form.get("a")
    n2 = request.form.get("b")
    return "La multiplicacion de {} y {} es {}".format(n1, n2,int(n1)*int(n2))

@app.route("/distancia", methods=['GET', 'POST'])
def distancia():
    operacion = None

    if request.method == 'POST':
        x1 = float(request.form.get("x1"))
        y1 = float(request.form.get("y1"))
        x2 = float(request.form.get("x2"))
        y2 = float(request.form.get("y2"))
        operacion = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    return render_template("distancia.html", resul=operacion)

@app.route("/figuras", methods=['GET', 'POST'])
def figura():
    total = None
    figura = None
    if request.method == 'POST':
        figura = request.form.get("figura")
        dato1 = float(request.form.get("dato1"))
        dato2 = float(request.form.get("dato2"))
        if figura == "cuadrado":
            total = dato1 * dato2
        elif figura == "triangulo":
            total = (dato1 * dato2) / 2
        elif figura == "pentagono":
            total = (5 * dato1 * dato2) / 2 
        elif figura == "circulo":
            total = math.pi * (dato1 ** 2)
    return render_template('figuras.html', total=round(total, 2) if total else None, figura=figura)


@app.route('/hola')
def func():
    return "<h1>Pollo loco</h1>"


@app.route('/user/<string:user>')
def user(user):
    return "<h1>dame 2 por favor, {}!</h1>".format(user)


@app.route('/square/<int:num>')
def square():
    return "<h1>El cuadrado de {} is {}.</h1>".format(num, num**2)

@app.route('/repeat/<string:text>/<int:times>')
def repeat(text, times):
    return "<h1>" + "".join([text] * times) + "</h1>"


@app.route('/suma/<float:a>/<float:b>')
def suma(a, b):
    return "<h1> La suma de {} and {} is {}.</h1>".format(a, b, a + b)





































if __name__ == '__main__':
    app.run(debug=True)