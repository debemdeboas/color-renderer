from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import re


app = Flask(__name__)
app.secret_key = 'uXqHqRA2eFxxzcskV586LoaU5Q7pfAom'
bootstrap = Bootstrap(app)
COLOR_VALIDATION_REGEX = re.compile(r'#([A-F]|\d){6}')
DICT_EXAMPLE_COLORS = {
    'red': '#FF0000',
    'green': '#00FF00',
    'blue': '#0000FF',
    'Neon Pink': '#FF10F0',
    'Pastel Pink': '#F8C8DC',
    'Iris': '#5D3FD3',
    'Bright Red': '#EE4B2B',
    'Chartreuse': '#DFFF00',
}

class ColorForm(FlaskForm):
    color = StringField('Desired color hex code',
                        description='Please use the following format: #{hex code}. The \'#\' can be omitted.',
                        validators=[DataRequired()])
    submit_btn = SubmitField('Render!')


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = ColorForm()
    
    if form.validate_on_submit():
        print()
        return redirect(url_for('render_color', id=form.color.data))

    return render_template('index.html', title='Color Renderer', color_form=form, dict_colors=DICT_EXAMPLE_COLORS)


@app.route('/color/<id>')
def render_color(id):
    if not isinstance(id, str):
        flash('Not a valid input type! (How?)')
        return redirect('/')

    id = id.upper()
    if not id.startswith('#'):
        id = f'#{id}'

    if not COLOR_VALIDATION_REGEX.fullmatch(id):
        flash('Invalid hex color format. Please try again.')
        return redirect('/')

    return render_template('color.html', title=f'Color {id}', J2_COLOR=id)


if __name__ == '__main__':
    app.run(threaded=True)

