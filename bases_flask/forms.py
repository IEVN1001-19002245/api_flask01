from wtforms import Form, EmailField
from wtforms import StringField, IntegerField, BooleanField, PasswordField, FloatField, Form, RadioField, SelectMultipleField
from wtforms import validators
from wtforms.widgets import ListWidget, CheckboxInput
from datetime import datetime
from wtforms import validators

class UserForm(Form):
    matricula=IntegerField('Matricula',[validators.DataRequired(message='El campo es requerido')])
    nombre= StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    apellido= StringField('Apellido', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    email= EmailField('Correo', [validators.Email(message='El correo no es valido')])

class DForm(Form):
    equis1=IntegerField('X1', [validators.DataRequired(message='Coordenada requerida')])
    igriega1=IntegerField('Y1', [validators.DataRequired(message='Coordenada requerida')])
    equis2=IntegerField('X2', [validators.DataRequired(message='Coordenada requerida')])
    igriega2=IntegerField('Y2', [validators.DataRequired(message='Coordenada requerida')])

class PizzaForm(Form):
    nombre = StringField('Nombre completo', [validators.DataRequired()])
    direccion = StringField('Dirección', [validators.DataRequired()])
    telefono = StringField('Teléfono', [validators.DataRequired()])
    tamanio = RadioField('Tamaño', choices=[('Chica', 'Chica'),('Mediana', 'Mediana'),('Grande', 'Grande')], 
                         default='Mediana')
    ingredientes = SelectMultipleField('Ingredientes', choices=[('Jamon', 'Jamón'), ('Piña', 'Piña'), ('Champiñones', 'Champiñones')],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    cantidad = IntegerField('Número de pizzas', [validators.InputRequired()])