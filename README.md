# Dieting_App

A personal diet tracking application with a Flask-based RESTful API, SQLite database, and a simple web UI. The app allows users to log meals and weights, view nutritional macros, track weight progress with charts, project weight loss, and generate custom diet/exercise/meal plans using the Google Gemini AI API.

## Features
- Log daily meals with calories, protein, carbs, and fat.
- Log body weight over time.
- Display today's macro totals.
- Visualize weight progress with a line chart.
- Project weekly and monthly weight loss based on a 1500-calorie diet.
- Generate beginner-friendly diet, exercise, or meal plans tailored to a 26-year-old, 5'11", 280 lbs male with a sedentary lifestyle, using Gemini AI.
- Local SQLite database for persistence.

## Prerequisites
- **Operating System**: Ubuntu (tested on 23.04+)
- **Python**: 3.12.3 or later
- **Tools**: 
  - `uv` (for virtual environment and package management)
  - `sqlite3` (command-line tool, optional for debugging)
- **Internet**: Required for Gemini API calls.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Butlchr17/Dieting_App.git
cd Dieting_App
2. Install Dependencies
Install uv if not already present:
bash

Collapse

Wrap

Run

Copy
curl -LsSf https://astral.sh/uv/install.sh | sh
Create and activate a virtual environment:
bash

Collapse

Wrap

Run

Copy
uv venv --seed venv
source venv/bin/activate
Install Python packages:
bash

Collapse

Wrap

Run

Copy
uv pip install flask flask-cors python-dotenv google-generativeai
Install SQLite CLI (optional):
bash

Collapse

Wrap

Run

Copy
sudo apt install sqlite3
3. Set Up Environment Variables
Create a .env file in the project root:
bash

Collapse

Wrap

Run

Copy
touch .env
Add your Google Gemini API key (obtain from https://aistudio.google.com/app/apikey):
text

Collapse

Wrap

Copy
GEMINI_API_KEY=your_api_key_here
Ensure .env is not committed to Git (already ignored in .gitignore).
4. Run the Application
With the virtual environment activated:
bash

Collapse

Wrap

Run

Copy
python app.py
The Flask server will start at http://127.0.0.1:5000.
5. Access the UI
Open index.html in a browser:
Directly: file:///home/grayfrog/workspace/github.com/Butlchr17/Dieting_App/index.html
Or serve locally for better CORS handling:
bash

Collapse

Wrap

Run

Copy
python -m http.server 8000
Then access http://127.0.0.1:8000/index.html.
Usage
Log Meal: Enter date, meal name, and nutritional values, then submit.
Log Weight: Enter date and weight in lbs, then submit.
View Macros: Click to see today's total calories, protein, carbs, and fat.
Weight Chart: Click to display a line chart of logged weights.
Project Loss: Calculate expected weekly and monthly weight loss.
Generate Plan: Select plan type (diet, exercise, meal) and add custom details (e.g., "low-carb") to get an AI-generated plan.
Development
Code Structure:
app.py: Flask backend with API endpoints.
index.html: Web UI with Chart.js for visualizations.
tracker.db: SQLite database (auto-created).
.env: Environment variables.
.gitignore: Excludes sensitive and temporary files.
Testing: Use the UI to log data and verify in tracker.db with sqlite3 tracker.db "SELECT * FROM meals;".
Debugging: Check server logs (python app.py output) and browser console (F12).
Contributing
Fork the repository.
Create a feature branch: git checkout -b feature-name.
Commit changes: git commit -m "Describe changes".
Push to the branch: git push origin feature-name.
Open a Pull Request.
License
[Add a license here, e.g., MIT] - Specify if open-source or private use only.

Notes
This is a development server (use Gunicorn or uWSGI for production).
The Gemini API uses the free tier; rate limits apply (e.g., 60 requests/min).
Consult a doctor before following generated plans.
Report issues or suggest features via GitHub Issues.
Acknowledgments
Built with Flask, SQLite, and Google Generative AI.
Inspired by personal weight loss tracking needs.