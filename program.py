
from dataclasses import dataclass, field


@dataclass
class Course:
    course_id: str
    course_name: str
    credits: int

    def get_course_info(self):
        return f"{self.course_id} - {self.course_name} ({self.credits} credits)"


@dataclass
class Enrollment:
    enrollment_id: int
    course: Course
    semester: str
    grade: float = None

    def assign_grade(self, grade):
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100.")
        self.grade = grade

    def get_enrollment_info(self):
        return f"{self.course.course_name} - Grade: {self.grade}"


@dataclass
class Student:
    student_id: int
    first_name: str
    last_name: str
    email: str
    enrollments: list = field(default_factory=list)

    def register_course(self, enrollment):
        if any(e.course.course_id == enrollment.course.course_id
               for e in self.enrollments):
            raise ValueError("Student is already registered.")
        self.enrollments.append(enrollment)

    def drop_course(self, course_id):
        self.enrollments = [
            e for e in self.enrollments
            if e.course.course_id != course_id
        ]

    def calculate_gpa(self):
        graded = [e for e in self.enrollments if e.grade is not None]

        total_credits = sum(e.course.credits for e in graded)

        if total_credits == 0:
            return 0.0

        weighted_grade = sum(
            e.grade * e.course.credits for e in graded
        )

        return round(weighted_grade / total_credits, 2)

    def get_student_info(self):
        return (
            f"Student: {self.first_name} {self.last_name}\n"
            f"ID: {self.student_id}\n"
            f"Email: {self.email}\n"
            f"GPA: {self.calculate_gpa()}"
        )


@dataclass
class Instructor:
    instructor_id: int
    name: str
    email: str
    courses: list = field(default_factory=list)

    def assign_course(self, course):
        if course not in self.courses:
            self.courses.append(course)


@dataclass
class Department:
    department_id: int
    name: str
    courses: list = field(default_factory=list)
    instructors: list = field(default_factory=list)

    def add_course(self, course):
        self.courses.append(course)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)


# Main program
if __name__ == "__main__":

    department = Department(1, "Computer Engineering")

    instructor = Instructor(
        101, "John Smith", "john@university.edu"
    )

    course1 = Course("CS101", "Python Programming", 4)
    course2 = Course("CS102", "Database Systems", 3)

    department.add_course(course1)
    department.add_course(course2)

    instructor.assign_course(course1)

    student = Student(
        1001, "Alex", "Brown", "alex@university.edu"
    )

    enrollment1 = Enrollment(1, course1, "Fall 2026")
    enrollment2 = Enrollment(2, course2, "Fall 2026")

    student.register_course(enrollment1)
    student.register_course(enrollment2)

    enrollment1.assign_grade(90)
    enrollment2.assign_grade(85)

    print(student.get_student_info())

    print("\nRegistered Courses:")
    for enrollment in student.enrollments:
        print(enrollment.get_enrollment_info())

