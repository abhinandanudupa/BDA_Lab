from cProfile import label
from cgitb import text
import mysql.connector
from tkinter import *
from tkinter import ttk
import re


# Some constants
HIGHEST_SEM = 8
LOWSET_SEM = 1
BRANCHES = ["CSE", "ISE", "ME", "AE", "ML", "ECE", "EEE"]
SECTIONS = ["A", "B", "C", "D"]
MAX_CGPA = 10
MIN_CGPA = 4


create_table = """CREATE TABLE student_data ( 
    usn CHAR(10),
	full_name VARCHAR(30),
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	branch VARCHAR(3),	
	semester INT,
	section CHAR(1),
	cgpa DOUBLE
);"""

add_entry = """INSERT INTO student_data VALUES (
	'1BM19CS000',
	'FULL NAME',
	'FIRST NAME',
	'LAST NAME',
	'CSE',
	6,
	'A',
	9.3
);"""

show_entries = """SELECT * FROM student_data;"""

add_entry_template = """INSERT INTO student_data VALUES (
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	{},
	'{}',
	{}
);"""

# Connect to the MySQL DB and
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="003_bda_p1"
)
# Test MySQL Object
# print(mydb)

# Get cursor
cursor = mydb.cursor()

# Initialise Tkinter Window and the frame
root = Tk()
root.geometry("300x350")
root.title(" Student Details Portal ")

# Student info
usn = ""
firstname = ""
lastname = ""
fullname = ""
branch = ""
semester = ""
section = ""
cgpa = ""

# Initialise text inout fields
usn_input = Text(root, height=1, width=11, bg="light yellow")
firstname_input = Text(root, height=1, width=20, bg="light yellow")
lastname_input = Text(root, height=1, width=20, bg="light yellow")
branch_input = Text(root, height=1, width=4, bg="light yellow")
semester_input = Text(root, height=1, width=2, bg="light yellow")
section_input = Text(root, height=1, width=2, bg="light yellow")
cgpa_input = Text(root, height=1, width=5, bg="light yellow")

# Initialise labels for the text fields
usn_label = Label(root, text="USN:", name="usn", bg="light cyan")
firstname_label = Label(root, text="Firstname:", name="firstname", bg="light cyan")
lastname_label = Label(root, text="Lastname:", name="lastname", bg="light cyan")
branch_label = Label(root, text="Branch:", name="branch", bg="light cyan")
semester_label = Label(root, text="Semester:", name="semester", bg="light cyan")
section_label = Label(root, text="Section:", name="section", bg="light cyan")
cgpa_label = Label(root, text="CGPA:", name="cgpa", bg="light cyan")


def get_student_info():
    """
    to get data from the text fields and store them in appropriate variables
    """
    global firstname, lastname, fullname, usn, branch, semester, section, cgpa
    firstname = firstname_input.get("1.0", "end-1c")
    lastname = lastname_input.get("1.0", "end-1c")
    fullname = f"{firstname} {lastname}"
    usn = usn_input.get("1.0", "end-1c")
    branch = branch_input.get("1.00", "end-1c")
    semester = semester_input.get("1.0", "end-1c")
    section = section_input.get("1.0", "end-1c")
    cgpa = cgpa_input.get("1.0", "end-1c")


def vaildate_field_with_pattern(pattern, field, reverse=False):
    """
    check if field matches pattern and return the value based on reverse
    """
    return_value = False
    if re.match(pattern, field):
        return_value = True
    else:
        return_value = False

    if not reverse:
        return return_value
    else:
        return not return_value


def validate_fields():
    """
    validate all fields
    """
    global firstname, lastname, fullname, usn, branch, semester, section, cgpa
    try:
        usn_check = vaildate_field_with_pattern(
            r"^1[Bb][mM]\d\d[a-zA-Z][A-Za-z]\d\d\d$", usn
        )
        usn = usn.upper()
        print(usn_check)

        firstname_check = vaildate_field_with_pattern(r"\s", firstname, True)
        firstname = firstname.upper()
        print(firstname_check)

        lastname_check = vaildate_field_with_pattern(r"\s", lastname, True)
        lastname = lastname.upper()
        print(lastname_check)

        branch_check = (
            vaildate_field_with_pattern(r"^[A-Za-z][A-Za-z][A-Za-z]?$", branch)
            and branch in BRANCHES
        )
        branch = branch.upper()
        print(branch_check)

        semester = int(semester)
        semester_check = LOWSET_SEM <= semester <= HIGHEST_SEM

        section_check = (
            vaildate_field_with_pattern(r"^[A-Za-z]$", section) and section in SECTIONS
        )
        section = section.upper()
        print(section_check)

        cgpa = float(cgpa)
        cgpa_check = MIN_CGPA < cgpa <= MAX_CGPA

        return (
            usn_check
            and firstname_check
            and lastname_check
            and branch_check
            and section_check
            and semester_check
            and cgpa_check
        )
    except TypeError:
        return False


def add_student_info():
    """
    execute an SQL query to add the entry after validating the fields and display the result
    """
    print(
        add_entry_template.format(
            usn, fullname, firstname, lastname, branch, semester, section, cgpa
        )
    )

    # Add status indicator to indicate the result of the query run on the GUI
    if validate_fields():
        cursor.execute(
            add_entry_template.format(
                usn, fullname, firstname, lastname, branch, semester, section, cgpa
            )
        )
        Label(
            root,
            text="Student details added succesfully.",
            name="details-validity",
            bg="light cyan",
        ).pack(side="bottom")
    else:
        Label(
            root,
            text="Invalid student details.\n Please check the details\n that you have entered.",
            name="details-validity",
            bg="light cyan",
        ).pack(side="bottom")


def add_student_callback():
    get_student_info()
    add_student_info()


# Initialise an add button with a callback
add_button = Button(root, height=2, width=20, text="add", command=add_student_callback)

# Add elements to the frame
Label(text="Enter the student's details:").pack()

usn_label.place(x=0, y=30)
usn_input.place(x=120, y=30)

firstname_label.place(x=0, y=60)
firstname_input.place(x=120, y=60)

lastname_label.place(x=0, y=90)
lastname_input.place(x=120, y=90)

branch_label.place(x=0, y=120)
branch_input.place(x=120, y=120)

semester_label.place(x=0, y=150)
semester_input.place(x=120, y=150)

section_label.place(x=0, y=180)
section_input.place(x=120, y=180)

cgpa_label.place(x=0, y=210)
cgpa_input.place(x=120, y=210)

add_button.pack(side="bottom")

# Run the GUI
mainloop()
