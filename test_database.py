from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from database.db_manager import DatabaseManager


class DatabaseManagerTests(unittest.TestCase):
    def test_initialize_and_add_task(self):
        with TemporaryDirectory() as temp:
            db = DatabaseManager(Path(temp) / "test.sqlite")
            db.initialize()
            task_id = db.add_task("Test task", "desc", "High", date.today(), "Work")
            tasks = db.get_all_tasks()
            self.assertGreater(task_id, 0)
            self.assertEqual(tasks[0]["title"], "Test task")

    def test_update_and_delete_task(self):
        with TemporaryDirectory() as temp:
            db = DatabaseManager(Path(temp) / "test.sqlite")
            db.initialize()
            task_id = db.add_task("Test task", "", "Medium", date.today(), "General")
            db.set_task_status(task_id, "Completed")
            self.assertEqual(db.get_all_tasks()[0]["status"], "Completed")
            db.delete_task(task_id)
            self.assertEqual(db.get_all_tasks(), [])


if __name__ == "__main__":
    unittest.main()
