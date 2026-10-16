# LifeLens AI
**Your Life. Your Goals. Your Growth.**

LifeLens AI is a local-first personal productivity and life-management web app built with Python, Streamlit, SQLite, Pandas, NumPy, and Matplotlib. Optional AI coaching uses the Gemini API. The dashboard is inspired by your reference screenshot: dark navy sidebar, white content area, rounded metric cards, colorful weekly chart, insight panel, schedule, and priority tasks. Streamlit controls widget rendering, so pixel-identical reproduction is not guaranteed.

## Windows + VS Code setup
1. Extract the ZIP and open the `LifeLens_AI_Professional` folder in VS Code.
2. Open **Terminal → New Terminal** and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

3. Open `http://localhost:8501` in your browser. If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If port 8501 is busy: `python -m streamlit run app.py --server.port 8502`.

## Gemini API setup
1. Copy `.env.example` to `.env` in the project root.
2. Add your key: `GEMINI_API_KEY=your_key_here`.
3. Optionally set `GEMINI_MODEL` to a model currently available to your account/region.
4. Restart Streamlit.

Use Google's official AI Studio and current Gemini API documentation to verify free-tier model availability, quotas, and pricing; these can change. Never commit `.env` or paste your key into source code. The rest of the app works without a key; the AI Coach returns a local-data fallback when the API is not configured or fails.

## Features included
- Dashboard with calculated task, focus, expense, workout, and personal growth indicators.
- Productivity: create/edit/complete/delete tasks, priorities, due dates, categories, tags, filters, overdue list, focus session history, daily schedule, daily goals, CSV export.
- Career: career goals and progress, skill inventory and chart, course/certification tracking, portfolio project tracking, job application tracking, AI learning-roadmap request.
- Finance: income and expenses in INR, category chart, monthly income-versus-expense chart, budgets, savings goals, CSV import/export, spending insights.
- Fitness: workout log and chart, sleep/water/activity wellness records, configurable personal goals.
- Mental growth: journal with delete, mood and gratitude check-ins, habit logs, optional AI reflection prompts.
- AI Life Coach: English, Hindi, Hinglish, data context, Gemini API and graceful fallback.
- Analytics: selectable 7/30/90-day reports, task/focus/workout charts, CSV report.
- Settings: display name and downloadable SQLite backup.

## Database and sample data
The SQLite database is created at `data/lifelens.db`. Demo records are added on first run if the task table is empty. They are examples for demonstration; remove the database while the app is stopped to reset it. Database tables include tasks, focus sessions, schedules, goals, career records, transactions, budgets, savings goals, workouts, wellness records, journal entries, mood check-ins, and habits.

## CSV import format
Finance CSV import requires `entry_date,kind,amount,category`; `note` is optional. Dates use `YYYY-MM-DD`, and `kind` must be `Income` or `Expense`.

## Tests
Run:

```powershell
python -m unittest discover -s tests -v
```

## Architecture
- `app.py`: Streamlit navigation, forms, dashboard, and charts.
- `database/db_manager.py`: SQLite schema, parameterized database operations, backup.
- `modules/`: productivity, finance, career, wellness, mental growth, analytics.
- `ai/life_coach.py`: Gemini client, user-context packaging, local fallback.
- `utils/`: data processing and CSV report generation.
- `tests/`: database and productivity tests.

## College presentation script
1. Introduce LifeLens AI and its personal-growth objective.
2. Show the dashboard metrics and explain that they are calculated from saved records.
3. Create and complete a priority task; show the weekly progress chart and overdue list.
4. Record a focus session and schedule item.
5. Record an expense, set a monthly budget, and view category/monthly charts.
6. Add a career goal and skill, then request a learning roadmap.
7. Record a workout, wellness entry, mood check-in, journal entry, and habit.
8. Show analytics and explain the growth-score formula.
9. Demonstrate Gemini setup and fallback behavior.
10. Explain the SQLite architecture, CSV workflows, and tests.

## Resume-ready description
**LifeLens AI — AI-Powered Personal Productivity Platform:** Developed a modular Python/Streamlit application with SQLite persistence, task and focus tracking, finance and budget management, career and skill tracking, wellness logs, journaling, CSV import/export, analytics, local backups, and optional Gemini API integration with graceful fallback behavior.

## Growth score
The dashboard's personal growth indicator is 50% task completion rate + 30% focus-target attainment (120 minutes, capped at 100%) + 20% when a workout is recorded. This is a transparent personal indicator, not a scientifically validated score.

## Limitations / future improvements
This is a college/portfolio project, not production-security-certified. Add authentication and per-user isolation before multi-user deployment. More advanced database migrations, broader CRUD workflows, a real Pomodoro timer, encryption for sensitive journal content, accessibility testing, and a security review are sensible next steps. Wellness and finance features are for personal tracking, not diagnosis or professional advice.
