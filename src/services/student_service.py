import json
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.models.student import Student


class StudentService:
    """Handles student CRUD operations and JSON persistence."""

    def __init__(self, data_file: str, logger):
        self.data_file = Path(data_file)
        self.logger = logger
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_data_file()

    def _ensure_data_file(self) -> None:
        if not self.data_file.exists():
            self._write_students([])

    def _read_students(self) -> List[Student]:
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return [Student.from_dict(item) for item in data]
        except json.JSONDecodeError as exc:
            self.logger.error("Invalid JSON data: %s", exc)
            raise ValueError("Student data file contains invalid JSON.") from exc
        except OSError as exc:
            self.logger.error("Could not read student data: %s", exc)
            raise RuntimeError("Could not read student data.") from exc

    def _write_students(self, students: List[Student]) -> None:
        try:
            with self.data_file.open("w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in students],
                    file,
                    indent=4
                )
        except OSError as exc:
            self.logger.error("Could not save student data: %s", exc)
            raise RuntimeError("Could not save student data.") from exc

    def get_all(self) -> List[Student]:
        return self._read_students()

    def get_by_id(self, student_id: str) -> Optional[Student]:
        student_id = student_id.strip().upper()
        return next(
            (student for student in self._read_students()
             if student.student_id.upper() == student_id),
            None
        )

    def add(self, student: Student) -> bool:
        students = self._read_students()

        if self.get_by_id(student.student_id):
            raise ValueError(f"Student ID {student.student_id} already exists.")

        students.append(student)
        self._write_students(students)
        self.logger.info("Added student %s", student.student_id)
        return True

    def update(self, student_id: str, updates: Dict[str, Any]) -> bool:
        students = self._read_students()
        student_id = student_id.strip().upper()

        for index, student in enumerate(students):
            if student.student_id.upper() == student_id:
                updated_data = student.to_dict()
                updated_data.update(updates)
                updated_data["student_id"] = student.student_id
                students[index] = Student.from_dict(updated_data)
                self._write_students(students)
                self.logger.info("Updated student %s", student_id)
                return True

        return False

    def delete(self, student_id: str) -> bool:
        students = self._read_students()
        student_id = student_id.strip().upper()
        filtered = [
            student for student in students
            if student.student_id.upper() != student_id
        ]

        if len(filtered) == len(students):
            return False

        self._write_students(filtered)
        self.logger.info("Deleted student %s", student_id)
        return True

    def search(self, keyword: str) -> List[Student]:
        keyword = keyword.strip().lower()
        return [
            student for student in self._read_students()
            if keyword in student.student_id.lower()
            or keyword in student.first_name.lower()
            or keyword in student.last_name.lower()
            or keyword in student.course.lower()
            or keyword in student.email.lower()
        ]
