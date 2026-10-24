from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


# -------------------------
# Student Result Model
# -------------------------
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    roll_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    subject1 = db.Column(db.Integer, nullable=False)
    subject2 = db.Column(db.Integer, nullable=False)
    subject3 = db.Column(db.Integer, nullable=False)
    subject4 = db.Column(db.Integer, nullable=False)
    subject5 = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer)
    average = db.Column(db.Float)
    grade = db.Column(db.String(5))
    result = db.Column(db.String(10))

    def calculate_result(self):
        """Calculate Total, Average, Grade and Result"""

        self.total = (
            self.subject1 +
            self.subject2 +
            self.subject3 +
            self.subject4 +
            self.subject5
        )

        self.average = round(self.total / 5, 2)

        # Grade Calculation
        if self.average >= 90:
            self.grade = "A+"
        elif self.average >= 80:
            self.grade = "A"
        elif self.average >= 70:
            self.grade = "B"
        elif self.average >= 60:
            self.grade = "C"
        elif self.average >= 50:
            self.grade = "D"
        else:
            self.grade = "F"

        # Pass / Fail
        marks = [
            self.subject1,
            self.subject2,
            self.subject3,
            self.subject4,
            self.subject5
        ]

        if min(marks) >= 35:
            self.result = "PASS"
        else:
            self.result = "FAIL"

    def __repr__(self):
        return f"<Student {self.roll_no} - {self.name}>"


# -------------------------
# Admin Model
# -------------------------
class Admin(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Admin {self.username}>"