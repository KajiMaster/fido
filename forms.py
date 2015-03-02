import ipaddress
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
            raise ValidationError('Only HTTP- or HTTPS-based URLs allowed!')
        if not pr.netloc:
            raise ValidationError('Relative URLs not allowed!')
        if '.' not in pr.netloc:
            raise ValidationError('Must specify a TLD!')
        if pr.netloc == 'localhost':
            raise ValidationError('You can\'t request a page on this site!')
        try:
            ip = ipaddress.ip_address(pr.netloc)
        except ValueError:
            pass
        else:
            if ip.is_loopback or ip.is_reserved or ip.is_private:
                raise ValidationError('Requests to that IP address are not allowed!')



