from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from database.db_manager import DatabaseManager


class ProductivityTests(unittest.TestCase):
    def test_focus_and_growth_score(self):
        with TemporaryDirectory() as temp:
            db = DatabaseManager(Path(temp) / "test.sqlite")
            db.initialize()
            today = date.today()
            db.add_task("Done task", "", "High", today, "Work")
            task_id = db.get_all_tasks()[0]["id"]
            db.set_task_status(task_id, "Completed")
            db.add_focus_session(today, 25)
            self.assertEqual(db.get_focus_minutes(today), 25)
            self.assertGreaterEqual(db.calculate_growth_score(today), 0)
            self.assertLessEqual(db.calculate_growth_score(today), 100)


if __name__ == "__main__":
    unittest.main()
