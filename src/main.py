from src.models.student import Student
from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.logger import setup_logger
from src.utils.validation import validate_student


def display_student(student: Student) -> None:
    print(
        f"{student.student_id} | {student.first_name} {student.last_name} | "
        f"Age: {student.age} | {student.course} | "
        f"{student.email} | {student.phone}"
    )


def add_student(service: StudentService, prefix: str) -> None:
    print("\n--- Add Student ---")
    student_id = input(f"Student ID ({prefix}-001 format): ").strip().upper()
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    age = input("Age: ").strip()
    course = input("Course: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()

    age_value = validate_student(
        first_name, last_name, age, course, email, phone
    )

    student = Student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
        age=age_value,
        course=course,
        email=email,
        phone=phone,
    )

    service.add(student)
    print("Student added successfully.")


def view_students(service: StudentService) -> None:
    print("\n--- Student Records ---")
    students = service.get_all()

    if not students:
        print("No student records found.")
        return

    for student in students:
        display_student(student)


def update_student(service: StudentService) -> None:
    print("\n--- Update Student ---")
    student_id = input("Student ID: ").strip().upper()
    existing = service.get_by_id(student_id)

    if not existing:
        print("Student not found.")
        return

    print("Press Enter to keep the existing value.")
    first_name = input(f"First name [{existing.first_name}]: ").strip()
    last_name = input(f"Last name [{existing.last_name}]: ").strip()
    age = input(f"Age [{existing.age}]: ").strip()
    course = input(f"Course [{existing.course}]: ").strip()
    email = input(f"Email [{existing.email}]: ").strip()
    phone = input(f"Phone [{existing.phone}]: ").strip()

    updates = {}
    if first_name:
        updates["first_name"] = first_name
    if last_name:
        updates["last_name"] = last_name
    if age:
        updates["age"] = validate_student(
            first_name or existing.first_name,
            last_name or existing.last_name,
            age,
            course or existing.course,
            email or existing.email,
            phone or existing.phone,
        )
    if course:
        updates["course"] = course
    if email:
        updates["email"] = email
    if phone:
        updates["phone"] = phone

    if not updates:
        print("No changes made.")
        return

    # Validate the complete resulting record.
    validate_student(
        updates.get("first_name", existing.first_name),
        updates.get("last_name", existing.last_name),
        str(updates.get("age", existing.age)),
        updates.get("course", existing.course),
        updates.get("email", existing.email),
        updates.get("phone", existing.phone),
    )

    service.update(student_id, updates)
    print("Student updated successfully.")


def delete_student(service: StudentService) -> None:
    print("\n--- Delete Student ---")
    student_id = input("Student ID: ").strip().upper()
    existing = service.get_by_id(student_id)

    if not existing:
        print("Student not found.")
        return

    confirmation = input(
        f"Delete {existing.first_name} {existing.last_name}? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        service.delete(student_id)
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def search_students(service: StudentService) -> None:
    print("\n--- Search Students ---")
    keyword = input("Enter ID, name, course, or email: ").strip()
    results = service.search(keyword)

    if not results:
        print("No matching students found.")
        return

    for student in results:
        display_student(student)


def main() -> None:
    config = load_config()
    logger = setup_logger(config["log_file"])
    service = StudentService(config["data_file"], logger)

    logger.info("Application started")
    print(f"\n=== {config['app_name']} ===")

    while True:
        print(
            "\n1. Add student\n"
            "2. View students\n"
            "3. Update student\n"
            "4. Delete student\n"
            "5. Search students\n"
            "6. Exit"
        )

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_student(service, config["student_id_prefix"])
            elif choice == "2":
                view_students(service)
            elif choice == "3":
                update_student(service)
            elif choice == "4":
                delete_student(service)
            elif choice == "5":
                search_students(service)
            elif choice == "6":
                logger.info("Application closed")
                print("Goodbye.")
                break
            else:
                print("Invalid option. Please choose 1-6.")
        except (ValueError, RuntimeError, FileNotFoundError) as exc:
            logger.error("Operation failed: %s", exc)
            print(f"Error: {exc}")
        except Exception as exc:
            logger.exception("Unexpected application error")
            print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    main()
