import wtforms
from wtforms import validators,StringField,FileField,SubmitField


class UploadForm(wtforms.Form):
    title=wtforms.StringField(validators.length(min=1,max=20))
    file=FileField('file')
    # submit=SubmitField('submit')

# class NewsForm(wtforms.Form):
#     file=FileField('file')

class UserForm(wtforms.Form):
    username=wtforms.StringField(validators.length(min=5,max=20))
    password=wtforms.StringField(validators.length(min=5,max=20))