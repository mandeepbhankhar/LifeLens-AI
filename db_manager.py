import sqlite3
from datetime import date, timedelta
from pathlib import Path


class DatabaseManager:
    """Owns SQLite connections and database-level operations for LifeLens AI."""

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self):
        schema = """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            priority TEXT NOT NULL DEFAULT 'Medium'
                CHECK(priority IN ('Low','Medium','High','Urgent')),
            due_date TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'General',
            status TEXT NOT NULL DEFAULT 'Pending'
                CHECK(status IN ('Pending','Completed')),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT
        );
        CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL CHECK(duration_minutes > 0),
            note TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            category TEXT NOT NULL,
            note TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_date TEXT NOT NULL,
            exercise_name TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL DEFAULT 0 CHECK(duration_minutes >= 0)
        );
        CREATE TABLE IF NOT EXISTS schedule_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schedule_date TEXT NOT NULL,
            schedule_time TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Personal'
        );
        """
        extra = """
        CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY,entry_date TEXT NOT NULL,kind TEXT NOT NULL CHECK(kind IN ('Income','Expense')),amount REAL NOT NULL CHECK(amount>=0),category TEXT NOT NULL,note TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS budgets(id INTEGER PRIMARY KEY,month TEXT UNIQUE NOT NULL,amount REAL NOT NULL CHECK(amount>=0));
        CREATE TABLE IF NOT EXISTS savings_goals(id INTEGER PRIMARY KEY,name TEXT NOT NULL,target_amount REAL NOT NULL,saved_amount REAL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS wellness_records(id INTEGER PRIMARY KEY,record_date TEXT UNIQUE NOT NULL,sleep_hours REAL NOT NULL,water_litres REAL NOT NULL,activity_minutes INTEGER NOT NULL,note TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS journal_entries(id INTEGER PRIMARY KEY,entry_date TEXT NOT NULL,entry_type TEXT NOT NULL,content TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS mood_checkins(id INTEGER PRIMARY KEY,checkin_date TEXT NOT NULL,mood TEXT NOT NULL,gratitude TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS habit_logs(id INTEGER PRIMARY KEY,habit_date TEXT NOT NULL,habit_name TEXT NOT NULL,completed INTEGER DEFAULT 0 CHECK(completed IN (0,1)));
        CREATE TABLE IF NOT EXISTS career_goals(id INTEGER PRIMARY KEY,title TEXT NOT NULL,target_date TEXT NOT NULL,details TEXT DEFAULT '',progress_percent INTEGER DEFAULT 0 CHECK(progress_percent BETWEEN 0 AND 100));
        CREATE TABLE IF NOT EXISTS skills(id INTEGER PRIMARY KEY,name TEXT UNIQUE NOT NULL,current_level INTEGER NOT NULL,target_level INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY,name TEXT NOT NULL,provider TEXT DEFAULT '',status TEXT NOT NULL,learning_hours REAL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS portfolio_projects(id INTEGER PRIMARY KEY,name TEXT NOT NULL,url TEXT DEFAULT '',description TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS job_applications(id INTEGER PRIMARY KEY,company TEXT NOT NULL,role TEXT NOT NULL,applied_date TEXT NOT NULL,status TEXT NOT NULL,notes TEXT DEFAULT '');
        CREATE TABLE IF NOT EXISTS daily_goals(id INTEGER PRIMARY KEY,goal_date TEXT UNIQUE NOT NULL,tasks_target INTEGER NOT NULL,focus_target_minutes INTEGER NOT NULL);
        """
        with self.connect() as conn:
            conn.executescript(schema)
            conn.executescript(extra)
            try: conn.execute("ALTER TABLE tasks ADD COLUMN tags TEXT DEFAULT ''")
            except sqlite3.OperationalError: pass
            conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)", ("user_name", "Alex"))

    def seed_demo_data_if_empty(self):
        with self.connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
            if count:
                return
            today = date.today()
            demo_tasks = [
                ("Finalize UI wireframe", "Review dashboard layout and spacing", "High", today.isoformat(), "Work", "Completed"),
                ("Read 10 pages", "Continue the current book", "Medium", today.isoformat(), "Learning", "Completed"),
                ("Practice Python OOP", "Review classes and exceptions", "High", today.isoformat(), "Learning", "Completed"),
                ("Plan weekly goals", "Choose the three most important outcomes", "Medium", today.isoformat(), "Personal", "Completed"),
                ("Review project roadmap", "Break the next milestone into tasks", "Medium", today.isoformat(), "Work", "Completed"),
                ("Complete database schema", "Create the initial SQLite schema", "Urgent", today.isoformat(), "Work", "Pending"),
                ("Walk for 20 minutes", "Short outdoor walk", "Low", today.isoformat(), "Health", "Pending"),
                ("Review expenses", "Check today's recorded spending", "Medium", today.isoformat(), "Finance", "Pending"),
            ]
            conn.executemany(
                """INSERT INTO tasks(title,description,priority,due_date,category,status)
                   VALUES(?,?,?,?,?,?)""", demo_tasks
            )
            for days_ago, tasks_done, focus in [
                (6, 3, 45), (5, 4, 60), (4, 6, 90), (3, 2, 35),
                (2, 5, 80), (1, 3, 50), (0, 5, 142)
            ]:
                day = (today - timedelta(days=days_ago)).isoformat()
                conn.execute(
                    "INSERT INTO focus_sessions(session_date,duration_minutes,note) VALUES(?,?,?)",
                    (day, focus, "Demo focus record"),
                )
                if days_ago:
                    for i in range(tasks_done):
                        conn.execute(
                            """INSERT INTO tasks(title,description,priority,due_date,category,status,created_at)
                               VALUES(?,?,?,?,?,?,?)""",
                            (f"Demo task {days_ago}-{i+1}", "", "Medium", day, "Demo", "Completed", day + " 09:00:00"),
                        )
            conn.execute(
                "INSERT INTO expenses(entry_date,amount,category,note) VALUES(?,?,?,?)",
                (today.isoformat(), 284, "Food", "Demo expense"),
            )
            conn.execute(
                "INSERT INTO workouts(workout_date,exercise_name,duration_minutes) VALUES(?,?,?)",
                (today.isoformat(), "Bodyweight workout", 25),
            )
            conn.execute(
                "INSERT INTO schedule_items(schedule_date,schedule_time,title,category) VALUES(?,?,?,?)",
                (today.isoformat(), "09:00", "Morning planning", "Personal"),
            )
            conn.execute(
                "INSERT INTO schedule_items(schedule_date,schedule_time,title,category) VALUES(?,?,?,?)",
                (today.isoformat(), "11:00", "Focused work session", "Work"),
            )
            conn.execute(
                "INSERT INTO schedule_items(schedule_date,schedule_time,title,category) VALUES(?,?,?,?)",
                (today.isoformat(), "13:00", "Lunch break", "Break"),
            )

    def get_setting(self, key, default=""):
        with self.connect() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
            return row["value"] if row else default

    def set_setting(self, key, value):
        with self.connect() as conn:
            conn.execute(
                """INSERT INTO settings(key,value) VALUES(?,?)
                   ON CONFLICT(key) DO UPDATE SET value=excluded.value""",
                (key, str(value)),
            )

    def add_task(self, title, description, priority, due_date, category):
        if not title or not title.strip():
            raise ValueError("Task title is required.")
        if priority not in {"Low", "Medium", "High", "Urgent"}:
            raise ValueError("Invalid priority.")
        due = due_date.isoformat() if isinstance(due_date, date) else str(due_date)
        with self.connect() as conn:
            cur = conn.execute(
                """INSERT INTO tasks(title,description,priority,due_date,category)
                   VALUES(?,?,?,?,?)""",
                (title.strip(), description, priority, due, category),
            )
            return cur.lastrowid

    def get_tasks_for_date(self, target_date):
        target = target_date.isoformat() if isinstance(target_date, date) else str(target_date)
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM tasks WHERE due_date=? ORDER BY id", (target,)).fetchall()
            return [dict(row) for row in rows]

    def get_all_tasks(self):
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM tasks ORDER BY due_date, CASE priority WHEN 'Urgent' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END, id").fetchall()
            return [dict(row) for row in rows]

    def set_task_status(self, task_id, status):
        if status not in {"Pending", "Completed"}:
            raise ValueError("Invalid task status.")
        with self.connect() as conn:
            conn.execute(
                "UPDATE tasks SET status=?, completed_at=CASE WHEN ?='Completed' THEN CURRENT_TIMESTAMP ELSE NULL END WHERE id=?",
                (status, status, int(task_id)),
            )

    def delete_task(self, task_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (int(task_id),))

    def add_focus_session(self, session_date, duration_minutes, note=""):
        if int(duration_minutes) <= 0:
            raise ValueError("Duration must be greater than zero.")
        day = session_date.isoformat() if isinstance(session_date, date) else str(session_date)
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO focus_sessions(session_date,duration_minutes,note) VALUES(?,?,?)",
                (day, int(duration_minutes), note),
            )

    def get_focus_minutes(self, target_date):
        target = target_date.isoformat() if isinstance(target_date, date) else str(target_date)
        with self.connect() as conn:
            return int(conn.execute(
                "SELECT COALESCE(SUM(duration_minutes),0) FROM focus_sessions WHERE session_date=?",
                (target,),
            ).fetchone()[0])

    def get_expense_total(self, target_date):
        target = target_date.isoformat() if isinstance(target_date, date) else str(target_date)
        with self.connect() as conn:
            new_total = conn.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE entry_date=? AND kind='Expense'", (target,)).fetchone()[0]
            old_total = conn.execute("SELECT COALESCE(SUM(amount),0) FROM expenses WHERE entry_date=?", (target,)).fetchone()[0]
            return float(new_total + old_total)

    def has_workout(self, target_date):
        target = target_date.isoformat() if isinstance(target_date, date) else str(target_date)
        with self.connect() as conn:
            return conn.execute("SELECT 1 FROM workouts WHERE workout_date=? LIMIT 1", (target,)).fetchone() is not None

    def calculate_growth_score(self, target_date):
        tasks = self.get_tasks_for_date(target_date)
        completion = (sum(t["status"] == "Completed" for t in tasks) / len(tasks) * 100) if tasks else 0
        focus = min(self.get_focus_minutes(target_date) / 120 * 100, 100)
        workout = 100 if self.has_workout(target_date) else 0
        # Transparent personal indicator, not a validated psychological or scientific score.
        return round(completion * 0.5 + focus * 0.3 + workout * 0.2)

    def get_weekly_productivity(self, target_date):
        days = [target_date - timedelta(days=i) for i in range(6, -1, -1)]
        result = []
        with self.connect() as conn:
            for day in days:
                d = day.isoformat()
                done = conn.execute(
                    "SELECT COUNT(*) FROM tasks WHERE due_date=? AND status='Completed'", (d,)
                ).fetchone()[0]
                focus = conn.execute(
                    "SELECT COALESCE(SUM(duration_minutes),0) FROM focus_sessions WHERE session_date=?", (d,)
                ).fetchone()[0]
                result.append({"day": day.strftime("%a"), "tasks_completed": int(done), "focus_minutes": int(focus)})
        return __import__("pandas").DataFrame(result)

    def get_priority_tasks(self, target_date):
        target = target_date.isoformat()
        with self.connect() as conn:
            rows = conn.execute(
                """SELECT * FROM tasks WHERE status='Pending'
                   ORDER BY CASE priority WHEN 'Urgent' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END,
                   due_date, id LIMIT 5"""
            ).fetchall()
            return [dict(row) for row in rows]

    def add_schedule_item(self, schedule_date, schedule_time, title, category):
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO schedule_items(schedule_date,schedule_time,title,category) VALUES(?,?,?,?)",
                (schedule_date.isoformat(), schedule_time, title, category),
            )

    def get_schedule(self, target_date):
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM schedule_items WHERE schedule_date=? ORDER BY schedule_time",
                (target_date.isoformat(),),
            ).fetchall()
            return [dict(row) for row in rows]

    def get_data_insights(self, target_date):
        tasks = self.get_tasks_for_date(target_date)
        pending = [t for t in tasks if t["status"] == "Pending"]
        high = [t for t in pending if t["priority"] in {"High", "Urgent"}]
        insights = []
        if high:
            insights.append(f"You have {len(high)} high-priority task(s) still pending today.")
        elif tasks:
            insights.append("No high-priority tasks are pending today. Consider preparing tomorrow's top task.")
        else:
            insights.append("Add tasks to begin seeing personalized productivity insights.")
        focus = self.get_focus_minutes(target_date)
        if focus >= 120:
            insights.append(f"You have recorded {focus} focus minutes today—great consistency.")
        elif focus > 0:
            insights.append(f"You have recorded {focus} focus minutes. A short, distraction-free session could help.")
        else:
            insights.append("No focus session is recorded today. Log one after your next focused work block.")
        spent = self.get_expense_total(target_date)
        if spent:
            insights.append(f"Today's recorded spending is ₹{spent:,.0f}. Add expenses consistently to reveal trends.")
        else:
            insights.append("No spending is recorded today. Record expenses if you want budget insights.")
        return insights

    def export_database_bytes(self):
        return self.db_path.read_bytes()

    def list_records(self, table, where=None, params=(), order_by="id DESC", limit=None):
        allowed = {"settings","tasks","focus_sessions","expenses","workouts","schedule_items","transactions","budgets","savings_goals","wellness_records","journal_entries","mood_checkins","habit_logs","career_goals","skills","courses","portfolio_projects","job_applications","daily_goals"}
        if table not in allowed: raise ValueError("Unsupported table")
        sql = f"SELECT * FROM {table}" + (" WHERE " + where if where else "") + " ORDER BY " + order_by
        args = tuple(params)
        if limit is not None: sql += " LIMIT ?"; args += (int(limit),)
        with self.connect() as conn: return [dict(r) for r in conn.execute(sql,args).fetchall()]

    def execute(self, sql, params=(), fetch=False):
        with self.connect() as conn:
            cur=conn.execute(sql,params)
            return [dict(r) for r in cur.fetchall()] if fetch else cur.rowcount

    def monthly_expense_total(self, target_date):
        month = target_date.strftime("%Y-%m")
        with self.connect() as conn:
            return float(conn.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE kind='Expense' AND substr(entry_date,1,7)=?",(month,)).fetchone()[0])
