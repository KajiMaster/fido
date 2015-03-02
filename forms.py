from urlparse import urlparse

from flask_wtf import Form
#from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import InputRequired, URL, ValidationError

class URLForm(Form):
    url = StringField('URL', validators=[InputRequired()])

    def validate_url(form, field):
        try:
            pr = urlparse(field.data)
        except Exception as e:
            raise ValidationError(e)
        if pr.scheme not in ('http', 'https'):
            raise ValidationError('Only HTTP- or HTTPS-based urls allowed!')
        if not pr.netloc:
            raise ValidationError('Relative URLs not allowed!')
        if '.' not in pr.netloc:
            raise ValidationError('Must specify a TLD!')



