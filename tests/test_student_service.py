import tempfile
import unittest
from pathlib import Path

from src.models.student import Student
from src.services.student_service import StudentService
from src.utils.logger import setup_logger


class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "students.json"
        log_file = Path(self.temp_dir.name) / "test.log"
        logger = setup_logger(str(log_file))
        self.service = StudentService(str(self.data_file), logger)

        self.student = Student(
            student_id="STU-001",
            first_name="Juan",
            last_name="Dela Cruz",
            age=20,
            course="BSIT",
            email="juan@example.com",
            phone="09123456789",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_get(self):
        self.service.add(self.student)
        result = self.service.get_by_id("STU-001")
        self.assertIsNotNone(result)
        self.assertEqual(result.first_name, "Juan")

    def test_update(self):
        self.service.add(self.student)
        self.assertTrue(
            self.service.update("STU-001", {"course": "BSCS"})
        )
        self.assertEqual(
            self.service.get_by_id("STU-001").course,
            "BSCS"
        )

    def test_delete(self):
        self.service.add(self.student)
        self.assertTrue(self.service.delete("STU-001"))
        self.assertIsNone(self.service.get_by_id("STU-001"))

    def test_search(self):
        self.service.add(self.student)
        results = self.service.search("BSIT")
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
