# Fitness Tracker (AAI-551 Project)

Lightweight fitness tracker combining nutrition and exercise logging with a Streamlit dashboard and simple JSON/CSV storage. Includes a calorie calculator and helper scripts to generate sample logs.

---

## Project Structure (important files)

- `main.py` — Streamlit entry point (navigation & pages). REQUIRED
- `auth.py` — Authentication (login/register using JSON storage). REQUIRED
- `storage.py` — JSON load/save helpers. REQUIRED
- `tracker.py` — Pages for logging nutrition and exercise and showing history. REQUIRED
- `visualize.py` — Dashboard and plotting utilities. REQUIRED
- `calories.py` — Calorie calculator page. REQUIRED
- `nutrition.py` — Backend for food data (loading and calorie calculation). REQUIRED for nutrition features
- `exercise.py` — Backend for exercise dataset and calorie calculation. REQUIRED for exercise features
- `nutrition_ui.py`, `exercise_ui.py` — Additional UI modules (Streamlit/Tk/Tkinter variants). RECOMMENDED
- `generate_sample_logs.py` — Script to auto-generate sample nutrition & exercise logs. OPTIONAL but helpful for demos
- `utils/` — helper package (`helpers.py`) for file paths and setup. REQUIRED
- `data/` — data directory (stores user logs: CSV/JSON). REQUIRED (include an empty folder or a `.gitkeep` file)
- `food/` — contains the food CSV dataset used by `nutrition.py`. REQUIRED for nutrition
- `exercise/` — contains `exercise_dataset.csv` used by `exercise.py`. REQUIRED for exercise

---

## Dependencies

Create a Python virtual environment and install dependencies. Minimal packages used:

- streamlit
- pandas
- matplotlib

You can create a `requirements.txt` with these entries and install via pip:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Example `requirements.txt` lines:

```
streamlit
pandas
matplotlib
```

---

## How to run

Recommended (Streamlit):

```powershell
streamlit run main.py
```

This will open the app in your browser (default http://localhost:8501). Using `python main.py` will also run parts of the app but Streamlit features (session state and full UI) work best with the `streamlit run` command.

---

## Generating sample data (optional)

A helper script `generate_sample_logs.py` is provided to populate `data/` with sample nutrition and exercise logs for the user `Rushi`.

Run it with:

```powershell
python generate_sample_logs.py
```

This creates/overwrites:
- `data/Rushi_nutrition.csv`
- `data/exercise_log.csv`

---

## Notes / Tips

- Keep the `data/` directory in source control (or add a `.gitkeep`) so the app has a place to write logs at runtime.
- If you see Streamlit warnings about `session_state` when running `python main.py`, use `streamlit run main.py` instead.
- Ensure the `food/` and `exercise/` folders contain the proper CSV datasets (`foodandcalories.csv` and `exercise_dataset.csv`) for nutrition and exercise features to work.

---

## Suggested git .gitignore entries

```
.venv/
__pycache__/
data/*.csv
data/*.json
.env
```
## Make sure to have utils folder in the same directory
