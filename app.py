import os
import logging
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurera loggning
logging.basicConfig(level=logging.INFO)

# Hantera Heroku's postgres:// till postgresql:// omdirigering
uri = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        app.logger.error(f"Error in home route: {str(e)}")
        return "An error occurred", 500

@app.route('/for-studenter')
def for_studenter():
    try:
        return render_template('for_studenter.html')
    except Exception as e:
        app.logger.error(f"Error in for_studenter route: {str(e)}")
        return "An error occurred", 500

@app.route('/publicera-jobb', methods=['GET', 'POST'])
def publicera_jobb():
    try:
        if request.method == 'POST':
            new_job = Job(
                title=request.form['title'],
                company=request.form['company'],
                description=request.form['description']
            )
            db.session.add(new_job)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('publicera_jobb.html')
    except Exception as e:
        app.logger.error(f"Error in publicera_jobb route: {str(e)}")
        return "An error occurred", 500

@app.route('/jobba-med-oss')
def jobba_med_oss():
    try:
        return render_template('jobba_med_oss.html')
    except Exception as e:
        app.logger.error(f"Error in jobba_med_oss route: {str(e)}")
        return "An error occurred", 500

@app.route('/om-oss')
def om_oss():
    try:
        return render_template('om_oss.html')
    except Exception as e:
        app.logger.error(f"Error in om_oss route: {str(e)}")
        return "An error occurred", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)