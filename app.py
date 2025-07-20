from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import date, datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)


# User constants
AGE = 26
HEIGHT_CM = 180
GENDER = 'male'
ACTIVITY_MULTIPLIER = 1.2
DAILY_CALORIES = 1500
START_WEIGHT_KG = 127


# Sample meals
SAMPLE_MEALS = [
    {'meal': 'Breakfast', 'calories': 350, 'protein': 25, 'carbs': 50, 'fat': 5},
    {'meal': 'Snack1', 'calories': 150, 'protein': 20, 'carbs': 15, 'fat': 0},
    {'meal': 'Lunch', 'calories': 600, 'protein': 65, 'carbs': 30, 'fat': 25},
    {'meal': 'Snack2', 'calories': 200, 'protein': 3, 'carbs': 25, 'fat': 10},
    {'meal': 'Dinner', 'calories': 400, 'protein': 30, 'carbs': 35, 'fat': 15}
]


# Gemini API key from environment (loaded from .env)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# Database setup
def init_db():
    try: 
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS meals
                (id INTEGER PRIMARY KEY, date TEXT, meal TEXT, calories REAL, protein REAL, carbs REAL, fat REAL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS weights
                (id INTEGER PRIMARY KEY, date TEXT, weight_lbs REAL)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Databas error: {e}")
    finally:
        conn.close()

init_db()


# BMR calculations
def calculate_bmr(weight_kg):
    if GENDER == 'male':
        return 10 * weight_kg + 6.25 * HEIGHT_CM - 5 * AGE + 5
    return 10 * weight_kg + 6.25 * HEIGHT_CM - 5 * AGE - 161

# TDEE calculations
def calculate_tdee(bmr):
    return bmr * ACTIVITY_MULTIPLIER

# Projected weight loss calculations
def project_loss(current_weight):
    bmr = calculate_bmr(current_weight)
    tdee = calculate_tdee(bmr)
    daily_deficit = tdee  - DAILY_CALORIES
    weekly_loss = (daily_deficit * 7) / 7700  # Approx 7700 cal/kg fat
    return weekly_loss * 2.20462, weekly_loss * 2.20462 * 4  # Weekly and Monthly projected losses in lbs


# API Endpoints

@app.route('/api/meals', methods=['POST'])
def log_meal():
    data = request.json
    required_fields = ['date', 'meal', 'calories', 'protein', 'carbs', 'fat']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    if len(data['meal']) > 100:
        return jsonify({'error': 'Meal name too long'}), 400
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
        if any(float(data[field]) < 0 for field in ['calories', 'protein', 'carbs', 'fat']):
            return jsonify({'error': 'Numeric fields must be non-negative'}), 400
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('''INSERT INTO meals (date, meal, calories, protein, carbs, fat) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (data['date'], data['meal'], data['calories'], data['protein'], data['carbs'], data['fat']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Meal logged'}), 201
    except (sqlite3.Error, ValueError) as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/meals', methods=['GET'])
def get_meals():
    date_param = request.args.get('date', date.today().isoformat())
    try:
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('SELECT * FROM meals WHERE date = ?', (date_param,))
        meals = c.fetchall()
        conn.close()
        return jsonify([{'id': m[0], 'date': m[1], 'meal': m[2], 'calories': m[3], 'protein': m[4], 
                         'carbs': m[5], 'fat': m[6]} for m in meals])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load_sample', methods=['POST'])
def load_sample():
    today = date.today().isoformat()
    try:
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        for meal in SAMPLE_MEALS:
            c.execute('''INSERT INTO meals (date, meal, calories, protein, carbs, fat) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (today, meal['meal'], meal['calories'], meal['protein'], meal['carbs'], meal['fat']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Sample plan loaded'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weights', methods=['POST'])
def log_weight():
    data = request.json
    if not all(field in data for field in ['date', 'weight_lbs']):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        datetime.strptime(data['date'], '%Y-%m-%d')
        if float(data['weight_lbs']) <= 0:
            return jsonify({'error': 'Weight must be positive'}), 400
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('INSERT INTO weights (date, weight_lbs) VALUES (?, ?)', 
                  (data['date'], data['weight_lbs']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Weight logged'}), 201
    except (sqlite3.Error, ValueError) as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weights', methods=['GET'])
def get_weights():
    try:
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('SELECT * FROM weights ORDER BY date')
        weights = c.fetchall()
        conn.close()
        return jsonify([{'date': w[1], 'weight_lbs': w[2]} for w in weights])
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project_loss', methods=['GET'])
def get_project_loss():
    try:
        conn = sqlite3.connect('tracker.db')
        c = conn.cursor()
        c.execute('SELECT weight_lbs FROM weights ORDER BY date DESC LIMIT 1')
        latest = c.fetchone()
        current_weight_lbs = latest[0] if latest else START_WEIGHT_KG * 2.20462
        conn.close()
        current_weight_kg = current_weight_lbs / 2.20462
        weekly, monthly = project_loss(current_weight_kg)
        return jsonify({'weekly': round(weekly, 1), 'monthly': round(monthly, 1)})
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_plan', methods=['POST'])
def generate_plan():
    if not GEMINI_API_KEY:
        return jsonify({'error': 'Gemini API key not set. Set GEMINI_API_KEY in .env file.'}), 400
    
    data = request.json
    plan_type = data.get('type')  # 'diet', 'exercise', or 'meal'
    details = data.get('details', '')  # Optional user details

    # Tailored prompt for safety and relevance
    prompt = (
        f"Generate a safe, beginner-friendly {plan_type} plan for a 26-year-old male, 5'11\" tall, "
        f"280 lbs, with a sedentary lifestyle aiming for gradual weight loss. "
        f"Include realistic goals, nutritional balance, and warnings to consult a doctor. "
        f"Custom details: {details}. Keep it concise, structured, and evidence-based."
    )
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return jsonify({'plan': response.text})
    except GoogleAPIError as e:
        return jsonify({'error': f"Gemini API error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({'error': f"Invalid input: {str(e)}"}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
