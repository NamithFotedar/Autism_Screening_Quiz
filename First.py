from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('autism_quiz.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age INTEGER NOT NULL,
                  total_score INTEGER NOT NULL,
                  result TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Quiz questions
questions = [
    "Does your child look at you when you call their name?",
    "How easy is it for your child to interact with other children?",
    "Does your child prefer to play alone?",
    "Can your child maintain a two-way conversation?",
    "Does your child have very strong interests in specific topics?",
    "Does your child understand and respond to social cues?",
    "Does your child show sensitivity to sounds, textures, or lights?",
    "Does your child engage in repetitive behaviors?",
    "Does your child have difficulty with changes in routine?",
    "Does your child make eye contact during conversations?"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        return render_template('quiz.html', name=name, age=age, questions=questions, enumerate=enumerate)
    return render_template('start.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    age = int(request.form['age'])

    # Calculate score
    score = 0
    for i in range(len(questions)):
        score += int(request.form.get(f'q{i}', 0))

    # Determine result based on score
    if score <= 10:
        result = "Low likelihood of autism spectrum traits"
    elif score <= 20:
        result = "Moderate likelihood of autism spectrum traits"
    else:
        result = "High likelihood of autism spectrum traits"

    # Store in database
    conn = sqlite3.connect('autism_quiz.db')
    c = conn.cursor()
    c.execute("INSERT INTO responses (name, age, total_score, result) VALUES (?, ?, ?, ?)",
              (name, age, score, result))
    conn.commit()
    conn.close()

    return render_template('result.html', name=name, score=score, result=result)

# HTML templates
templates = {
    'index.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Autism Screening Quiz</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            background-color: #f0f0f0; 
        }
        .container { 
            max-width: 800px; 
            width: 100%; 
            padding: 40px; 
            background-color: white; 
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); 
            border-radius: 5px;
            animation: fade-in 0.5s;
        }
        h1 {
            margin-top: 0;
            opacity: 0;
            animation: slide-up 0.5s forwards;
        }
        p {
            line-height: 1.8;
            color: #444;
            opacity: 0;
            animation: slide-up 0.5s forwards 0.2s;
        }
        .btn { 
            padding: 12px 24px; 
            background: #4CAF50; 
            color: white; 
            text-decoration: none; 
            border-radius: 5px;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            opacity: 0;
            animation: slide-up 0.5s forwards 0.4s;
        }
        .btn:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .info-card {
            background: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            opacity: 0;
            animation: slide-up 0.5s forwards 0.3s;
        }
        .info-card h2 {
            margin-top: 0;
            color: #2e7d32;
        }
        .disclaimer {
            font-size: 0.9em;
            color: #666;
            border-left: 4px solid #4CAF50;
            padding-left: 15px;
            margin: 20px 0;
            opacity: 0;
            animation: slide-up 0.5s forwards 0.5s;
        }

        @keyframes fade-in {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes slide-up {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to the Autism Screening Quiz</h1>
        <div class="info-card">
            <h2>About This Screening Tool</h2>
            <p>This quiz is designed to help identify potential autism spectrum traits in individuals. The questions cover various aspects of behavior, social interaction, and communication patterns.</p>
        </div>
        <p class="disclaimer">Please note that this is not a diagnostic tool and should not replace professional medical advice. The results should be discussed with qualified healthcare professionals for proper evaluation.</p>
        <a href="/quiz" class="btn">Start Quiz</a>
    </div>
</body>
</html>
    ''',

    'start.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Parent Information - Autism Screening Quiz</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            background-color: #f0f0f0; 
        }
        .container { 
            max-width: 800px; 
            width: 100%; 
            padding: 40px; 
            background-color: white; 
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); 
            border-radius: 5px;
            animation: fade-in 0.5s;
        }
        .form-group { 
            margin-bottom: 20px; 
            opacity: 0;
            animation: slide-up 0.5s forwards;
        }
        .form-group:nth-child(2) {
            animation-delay: 0.2s;
        }
        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        .form-helper {
            font-size: 0.9em;
            color: #666;
            margin-top: 4px;
        }
        input[type="text"], input[type="number"] { 
            padding: 12px; 
            width: 100%; 
            max-width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
        }
        .btn { 
            padding: 12px 24px; 
            background: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            opacity: 0;
            animation: slide-up 0.5s forwards 0.4s;
        }
        .btn:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        .info-note {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
            opacity: 0;
            animation: slide-up 0.5s forwards 0.1s;
        }
        .error {
            color: #d32f2f;
            font-size: 0.9em;
            margin-top: 4px;
            display: none;
        }
        input:invalid + .error {
            display: block;
        }

        @keyframes fade-in {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes slide-up {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Parent Information</h1>
        <div class="info-note">
            <strong>Note:</strong> This screening quiz is designed for parents to evaluate their children for potential autism spectrum traits. Please ensure you are a parent or legal guardian before proceeding.
        </div>
        <form action="/quiz" method="post" onsubmit="return validateForm()">
            <div class="form-group">
                <label>Your Name (Parent/Guardian):</label>
                <input type="text" name="name" required>
                <div class="form-helper">Please enter your full name as the parent/guardian</div>
            </div>
            <div class="form-group">
                <label>Your Age:</label>
                <input type="number" name="age" required min="30" max="100">
                <div class="form-helper">Must be at least 30 years old to take this assessment</div>
                <div class="error">Age must be at least 30 years</div>
            </div>
            <input type="submit" value="Continue to Quiz" class="btn">
        </form>
    </div>

    <script>
        function validateForm() {
            const age = document.querySelector('input[name="age"]').value;
            if (age < 30) {
                alert('You must be at least 30 years old to take this assessment.');
                return false;
            }
            return true;
        }
    </script>
</body>
</html>
    ''',

    'quiz.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Autism Screening Quiz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 800px;
            width: 100%;
            padding: 40px;
            background-color: white;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }
        .progress-container {
            width: 100%;
            background-color: #f0f0f0;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .progress-bar {
            width: 0%;
            height: 20px;
            background-color: #4CAF50;
            border-radius: 5px;
            transition: width 0.3s ease-in-out;
        }
        .progress-text {
            text-align: center;
            margin-bottom: 10px;
            font-size: 14px;
            color: #666;
        }
        .question-card h3 {
            margin-top: 0;
        }
        .options {
            margin-left: 20px;
            margin-bottom: 20px;
        }
        .options label {
            display: block;
            margin: 10px 0;
            cursor: pointer;
        }
        .options input[type="radio"] {
            margin-right: 10px;
        }
        .navigation-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        .btn {
            padding: 10px 20px;
            background: linear-gradient(145deg, #4CAF50, #66BB6A);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            flex: 1;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.1s ease, box-shadow 0.2s ease;
        }
        .btn:hover {
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        .btn:active {
            transform: scale(0.95);
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
        }
        .btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
            box-shadow: none;
        }
        #prevButton {
            background: #666;
        }
        .fade-in {
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="progress-text">Question 1 of {{ questions|length }}</div>
        <div class="progress-container">
            <div class="progress-bar" id="progressBar"></div>
        </div>

        <form action="/result" method="post" id="quizForm">
            <input type="hidden" name="name" value="{{ name }}">
            <input type="hidden" name="age" value="{{ age }}">

            {% for i, question in enumerate(questions) %}
            <div class="question-card fade-in" {% if i == 0 %}style="display:block"{% else %}style="display:none"{% endif %} id="question{{ i }}">
                <h3>{{ i+1 }}. {{ question }}</h3>
                <div class="options">
                    <label><input type="radio" name="q{{ i }}" value="0" required> Never</label>
                    <label><input type="radio" name="q{{ i }}" value="1"> Sometimes</label>
                    <label><input type="radio" name="q{{ i }}" value="2"> Often</label>
                    <label><input type="radio" name="q{{ i }}" value="3"> Always</label>
                </div>
            </div>
            {% endfor %}

            <div class="navigation-buttons">
                <button type="button" id="prevButton" class="btn" disabled>Previous</button>
                <button type="button" id="nextButton" class="btn">Next</button>
            </div>
        </form>
    </div>

    <script>
        const questionCards = document.querySelectorAll('.question-card');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.querySelector('.progress-text');
        const form = document.querySelector('form');
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        const totalQuestions = {{ questions|length }};
        let currentQuestion = 0;

        function updateProgress() {
            let answeredQuestions = 0;
            questionCards.forEach((card, index) => {
                const radios = form.querySelectorAll(`input[name="q${index}"]:checked`);
                if (radios.length > 0) answeredQuestions++;
            });

            const progress = (answeredQuestions / totalQuestions) * 100;
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${answeredQuestions} of ${totalQuestions} questions answered`;
        }

        function showQuestion(index) {
            questionCards.forEach((card, i) => {
                card.classList.remove('fade-in');
                card.style.display = i === index ? 'block' : 'none';
            });

            prevButton.disabled = index === 0;

            if (index === totalQuestions - 1) {
                nextButton.textContent = 'Submit';
                nextButton.type = 'submit';
            } else {
                nextButton.textContent = 'Next';
                nextButton.type = 'button';
            }

            progressText.textContent = `Question ${index + 1} of ${totalQuestions}`;
            questionCards[index].classList.add('fade-in');
        }

        function validateCurrentQuestion() {
            const currentRadios = form.querySelectorAll(`input[name="q${currentQuestion}"]:checked`);
            return currentRadios.length > 0;
        }

        prevButton.addEventListener('click', () => {
            if (currentQuestion > 0) {
                currentQuestion--;
                showQuestion(currentQuestion);
            }
        });

        nextButton.addEventListener('click', () => {
            if (nextButton.type === 'submit') {
                if (validateCurrentQuestion()) {
                    form.submit();
                } else {
                    alert('Please answer the current question before submitting.');
                }
            } else if (validateCurrentQuestion()) {
                currentQuestion++;
                showQuestion(currentQuestion);
            } else {
                alert('Please answer the current question before proceeding.');
            }
        });

        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', updateProgress);
        });

        updateProgress();
        showQuestion(0);
    </script>
</body>
</html>

    ''',

    'result.html': '''
<!DOCTYPE html>
<html>
<head>
    <title>Quiz Results</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            background-color: #f0f0f0; 
        }
        .container { 
            max-width: 800px; 
            width: 100%; 
            padding: 40px; 
            background-color: white; 
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); 
            border-radius: 5px;
            animation: fade-in 0.5s;
        }
        .result { 
            padding: 25px; 
            background: #f8f8f8; 
            border-radius: 8px; 
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            opacity: 0;
            animation: slide-up 0.5s forwards 0.2s;
        }
        .btn { 
            padding: 12px 24px; 
            background: #4CAF50; 
            color: white; 
            text-decoration: none; 
            border-radius: 5px;
            display: inline-block;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            opacity: 0;
            animation: slide-up 0.5s forwards 0.4s;
        }
        .btn:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        h1 {
            margin-bottom: 30px;
        }
        .score {
            font-size: 24px;
            color: #4CAF50;
            margin: 15px 0;
        }
        .note {
            margin-top: 20px;
            padding: 15px;
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            border-radius: 4px;
        }

        @keyframes fade-in {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes slide-up {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Quiz Results</h1>
        <div class="result">
            <h2>Hello {{ name }},</h2>
            <p class="score">Your score: {{ score }}/30</p>
            <p>Result: {{ result }}</p>
            <p class="note"><strong>Important Note:</strong> This screening tool is not a diagnostic instrument. A proper diagnosis can only be made by qualified healthcare professionals.</p>
        </div>
        <a href="/" class="btn">Take Quiz Again</a>
    </div>
</body>
</html>
    '''
}

if __name__ == '__main__':
    init_db()
    app.run(debug=True)