from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import URL

class URLForm(Form):
    url = StringField(i"URL", validators=[URL()])


