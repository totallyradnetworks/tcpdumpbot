from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional
import tcpdump_flask

#import threading
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tcpdumpbotsecretkey'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.before_request
def before_request_func():
    tcpdump_flask.tcpdump_test()

@app.route('/', methods=['GET', 'POST'])
def index():
    if tcpdump_flask.tcpdump_is_running() == False:
        form = tcpdumpform()
        if form.validate_on_submit():
            filename = form.file_name.data
            tcpdump_flask.set_pcap_filename(filename)
            tcpdump_flask.tcpdump_run()
            form = tcpdumpformstop()
            return render_template('index.html', form=form, current_time=datetime.utcnow(), tcpdump_on=True, filename=filename)
        return render_template('index.html', form=form, current_time=datetime.utcnow(), tcpdump_on=False)
    else:
        form = tcpdumpformstop()
        if form.is_submitted():
            tcpdump_flask.kill_process()
            form = tcpdumpform()
            return render_template('index.html', form=form, current_time=datetime.utcnow(), tcpdump_on=False)
        return render_template('index.html', form=form, current_time=datetime.utcnow(), tcpdump_on=True, filename=filename)
        


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/tcpdump_run')
def tcpdump_run():
    #thread = threading.Thread(target=tcpdump_flask.tcpdump_run())
    #thread.start()
    tcpdump_flask.tcpdump_run()
    return redirect('/')

@app.route('/tcpdump_stop')
def tcpdump_stop():
    tcpdump_flask.kill_process()
    return redirect('/')

@app.route('/update_tcpdump_command')
def update_tcpdump_command():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

class tcpdumpform(FlaskForm):
    file_name = StringField('What .pcap filename would you like to use?', validators=[DataRequired()])
    submit = SubmitField('Start TCPDUMPBOT')

class tcpdumpformstop(FlaskForm):
    submit = SubmitField('Stop TCPDUMPBOT')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
