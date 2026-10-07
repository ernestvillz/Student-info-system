from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Student:
    """Represents a student record."""

    student_id: str
    first_name: str
    last_name: str
    age: int
    course: str
    email: str
    phone: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert the student object to a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Create a Student object from a dictionary."""
        return cls(
            student_id=str(data["student_id"]),
            first_name=str(data["first_name"]),
            last_name=str(data["last_name"]),
            age=int(data["age"]),
            course=str(data["course"]),
            email=str(data["email"]),
            phone=str(data["phone"]),
        )
