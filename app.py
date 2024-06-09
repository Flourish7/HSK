from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import openai
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your model
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(50))
    school_year = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(50))
    aspirations = db.Column(db.String(50))
    query = db.Column(db.Text)
    response = db.Column(db.Text)

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    age = data.get('age')
    school_year = data.get('school_year')
    subject = data.get('subject')
    topic = data.get('topic')
    aspirations = data.get('aspirations')
    query_text = data.get('query')
    
    # Construct the GPT prompt
    prompt = f"Age: {age}, School Year: {school_year}, Subject: {subject}, Topic: {topic}, Aspirations: {aspirations}. {query_text}"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Extract and return the response text
    gpt_response = response.choices[0].text.strip()

    # Save the query and response to the database
    new_query = Query(
        age=age,
        school_year=school_year,
        subject=subject,
        topic=topic,
        aspirations=aspirations,
        query=query_text,
        response=gpt_response
    )
    db.session.add(new_query)
    db.session.commit()

    return jsonify({'response': gpt_response})

if __name__ == '__main__':
    app.run(debug=True)
