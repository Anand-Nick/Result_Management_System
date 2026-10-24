from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Student, Admin
from werkzeug.security import check_password_hash

app = Flask(__name__)

# -------------------------------
# Configuration
# -------------------------------
app.config["SECRET_KEY"] = "resultmanagement123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///result.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("home.html")


# -------------------------------
# About Page
# -------------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------------
# Admin Login
# -------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):

            session["admin"] = username

            flash("Login Successful", "success")

            return redirect(url_for("dashboard"))

        else:

            flash("Invalid Username or Password", "danger")

    return render_template("login.html")


# -------------------------------
# Logout
# -------------------------------
@app.route("/logout")
def logout():

    session.pop("admin", None)

    flash("Logged Out Successfully", "success")

    return redirect(url_for("login"))


# -------------------------------
# Dashboard
# -------------------------------
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    total_students = Student.query.count()

    total_cse = Student.query.filter_by(
        department="CSE"
    ).count()

    total_it = Student.query.filter_by(
        department="IT"
    ).count()

    total_ece = Student.query.filter_by(
        department="ECE"
    ).count()

    total_mech = Student.query.filter_by(
        department="MECH"
    ).count()

    total_civil = Student.query.filter_by(
        department="CIVIL"
    ).count()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_cse=total_cse,
        total_it=total_it,
        total_ece=total_ece,
        total_mech=total_mech,
        total_civil=total_civil
    )


# -------------------------------
# Add Student Result
# -------------------------------
@app.route("/add", methods=["GET", "POST"])
def add_result():

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        student = Student(

            roll_no=request.form["roll_no"],

            name=request.form["name"],

            department=request.form["department"],

            semester=int(request.form["semester"]),

            subject1=int(request.form["subject1"]),

            subject2=int(request.form["subject2"]),

            subject3=int(request.form["subject3"]),

            subject4=int(request.form["subject4"]),

            subject5=int(request.form["subject5"])
        )

        # Calculate total, average, grade, result
        student.calculate_result()

        db.session.add(student)

        db.session.commit()

        flash("Student Result Added Successfully", "success")

        return redirect(url_for("view_results"))

    return render_template("add_result.html")
# -------------------------------
# View All Results
# -------------------------------
@app.route("/results")
def view_results():

    if "admin" not in session:
        return redirect(url_for("login"))

    students = Student.query.order_by(Student.id.desc()).all()

    return render_template(
        "view_results.html",
        students=students
    )


# -------------------------------
# Search Student
# -------------------------------
@app.route("/search", methods=["GET", "POST"])
def search():

    if "admin" not in session:
        return redirect(url_for("login"))

    students = []

    if request.method == "POST":

        keyword = request.form["keyword"]

        students = Student.query.filter(

            (Student.roll_no.contains(keyword)) |
            (Student.name.contains(keyword))

        ).all()

    return render_template(
        "view_results.html",
        students=students
    )


# -------------------------------
# Edit Result
# -------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_result(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        student.roll_no = request.form["roll_no"]
        student.name = request.form["name"]
        student.department = request.form["department"]
        student.semester = int(request.form["semester"])

        student.subject1 = int(request.form["subject1"])
        student.subject2 = int(request.form["subject2"])
        student.subject3 = int(request.form["subject3"])
        student.subject4 = int(request.form["subject4"])
        student.subject5 = int(request.form["subject5"])

        # Recalculate marks
        student.calculate_result()

        db.session.commit()

        flash("Student Result Updated Successfully", "success")

        return redirect(url_for("view_results"))

    return render_template(
        "edit_result.html",
        student=student
    )


# -------------------------------
# Delete Result
# -------------------------------
@app.route("/delete/<int:id>")
def delete_result(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)

    db.session.commit()

    flash("Student Result Deleted Successfully", "warning")

    return redirect(url_for("view_results"))


# -------------------------------
# View Individual Student Result
# -------------------------------
@app.route("/student/<roll_no>")
def student_result(roll_no):

    student = Student.query.filter_by(
        roll_no=roll_no
    ).first_or_404()

    return render_template(
        "student_result.html",
        student=student
    )
# -------------------------------
# Department Wise Pages
# -------------------------------

@app.route("/cse")
def cse():

    students = Student.query.filter_by(
        department="CSE"
    ).all()

    return render_template(
        "cse.html",
        students=students
    )


@app.route("/it")
def it():

    students = Student.query.filter_by(
        department="IT"
    ).all()

    return render_template(
        "it.html",
        students=students
    )


@app.route("/ece")
def ece():

    students = Student.query.filter_by(
        department="ECE"
    ).all()

    return render_template(
        "ece.html",
        students=students
    )


@app.route("/civil")
def civil():

    students = Student.query.filter_by(
        department="CIVIL"
    ).all()

    return render_template(
        "civil.html",
        students=students
    )


@app.route("/mech")
def mech():

    students = Student.query.filter_by(
        department="MECH"
    ).all()

    return render_template(
        "mech.html",
        students=students
    )


# -------------------------------
# Initialize Database
# -------------------------------
with app.app_context():
    db.create_all()


# -------------------------------
# Run Flask Application
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)