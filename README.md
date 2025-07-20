# Dieting_App

A personal diet tracking application with a Flask-based RESTful API, SQLite database, and a simple web UI. The app allows users to log meals and weights, view nutritional macros, track weight progress with charts, project weight loss, and generate custom diet/exercise/meal plans using the Google Gemini AI API.

---

## Features

- Log daily meals with calories, protein, carbs, and fat.
- Log body weight over time.
- Display today's macro totals.
- Visualize weight progress with a line chart.
- Project weekly and monthly weight loss based on a 1500-calorie diet.
- Generate beginner-friendly diet, exercise, or meal plans tailored to a 26-year-old, 5'11", 280 lbs male with a sedentary lifestyle using Gemini AI.
- Local SQLite database for persistence.

---

## Prerequisites

- **Operating System**: Ubuntu (tested on 23.04+)
- **Python**: 3.12.3 or later
- **Tools**:
  - [`uv`](https://github.com/astral-sh/uv) for virtual environment and dependency management
  - `sqlite3` CLI (optional, for debugging)
- **Internet Access**: Required for Gemini API

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Butlchr17/Dieting_App.git
cd Dieting_App
```

### 2. Install Dependencies

**Install `uv` (if not already installed):**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Create and activate a virtual environment:**

```bash
uv venv --seed venv
source venv/bin/activate
```

**Install Python packages:**

```bash
uv pip install flask flask-cors python-dotenv google-generativeai
```

**(Optional) Install SQLite CLI:**

```bash
sudo apt install sqlite3
```

---

### 3. Set Up Environment Variables

**Create a `.env` file in the project root:**

```bash
touch .env
```

**Add your Gemini API key to the `.env` file:**

```
GEMINI_API_KEY=your_api_key_here
```

> You can get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

The `.env` file is already listed in `.gitignore`.

---

### 4. Run the Application

With your virtual environment activated:

```bash
python app.py
```

The Flask server will start at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 5. Access the UI

**Option 1**: Open the file directly in a browser:

```
file:///full/path/to/Dieting_App/index.html
```

**Option 2**: Serve with Python for proper CORS handling:

```bash
python -m http.server 8000
```

Then go to [http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html)

---

## Usage

- **Log Meal**: Enter date, meal name, and nutritional values; then submit.
- **Log Weight**: Enter date and body weight in pounds; then submit.
- **View Macros**: Shows today's total intake of calories, protein, carbs, and fat.
- **Weight Chart**: Displays weight history using a line chart.
- **Project Loss**: Estimates weekly/monthly weight loss under a 1500-calorie diet.
- **Generate Plan**: Select a plan type (diet, exercise, meal) and optionally enter preferences (e.g., "low-carb").

---

## Development

### Code Structure

- `app.py`: Flask backend with REST API routes
- `index.html`: Web UI with embedded JavaScript and Chart.js
- `tracker.db`: SQLite database (auto-generated)
- `.env`: Environment variables
- `.gitignore`: Ignores sensitive/temporary files

### Debugging & Testing

- **Database**: View entries with:
  ```bash
  sqlite3 tracker.db "SELECT * FROM meals;"
  ```
- **Server Logs**: Output appears in the terminal running `app.py`
- **Frontend Debug**: Use browser DevTools (F12 → Console/Network tabs)

---

## Contributing

1. Fork this repo
2. Create a feature branch:  
   ```bash
   git checkout -b your-feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to GitHub:  
   ```bash
   git push origin your-feature-name
   ```
5. Open a Pull Request

---

## License

License MIT License - feel free to use and modify.

---

## Notes

- This runs on Flask’s development server — for production, use Gunicorn or uWSGI.
- Google Gemini free-tier limits apply (e.g., 60 requests/minute).
- AI-generated plans are for educational use — consult a physician before following any advice.

---

## Acknowledgments

- Built with **Flask**, **SQLite**, **Chart.js**, and **Google Generative AI**
- Inspired by personal weight loss tracking needs
