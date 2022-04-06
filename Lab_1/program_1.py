# Import libraries
import mysql.connector
import re

# Some constants
HIGHEST_SEM = 8
LOWSET_SEM = 1
BRANCHES = ["CSE", "ISE", "ME", "AE", "ML", "ECE", "EEE"]
SECTIONS = ["A", "B", "C", "D"]
MAX_CGPA = 10
MIN_CGPA = 4

# Student info
usn = ""
firstname = ""
lastname = ""
fullname = ""
branch = ""
semester = ""
section = ""
cgpa = ""
# Initial MySQL Object
mydb = mysql.connector.connect(
    host="localhost", user="root", password="password", database="003_bda_p1"
)

# Test the creation of the object
print(mydb)

# Get cursor
cursor = mydb.cursor()

# SQL query to test table creation
create_table = """CREATE TABLE student_data ( usn CHAR(10),
	full_name VARCHAR(30),
	first_name VARCHAR(30),
	last_name VARCHAR(30),
	branch VARCHAR(3),	
	semester INT,
	section CHAR(1),
	cgpa DOUBLE
);"""

# SQL query to test inserting an entry
add_entry = """INSERT INTO student_data VALUES (
	'{}',
	'{}',
	'{}',
	'{}',
	'{}',
	{},
	'{}',
	{}
);"""

# SQL query to show table contents
show_entries = """SELECT * FROM student_data;"""


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
        # print(usn_check)

        firstname_check = vaildate_field_with_pattern(r"\s", firstname, True)
        firstname = firstname.upper()
        # print(firstname_check)

        lastname_check = vaildate_field_with_pattern(r"\s", lastname, True)
        lastname = lastname.upper()
        # print(lastname_check)

        branch_check = (
            vaildate_field_with_pattern(r"^[A-Za-z][A-Za-z][A-Za-z]?$", branch)
            and branch in BRANCHES
        )
        branch = branch.upper()
        # print(branch_check)

        semester = int(semester)
        semester_check = LOWSET_SEM <= semester <= HIGHEST_SEM

        section_check = (
            vaildate_field_with_pattern(r"^[A-Za-z]$", section) and section in SECTIONS
        )
        section = section.upper()
        # print(section_check)

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


def get_student_info():
    """
    get student info through the terminal
    """
    global firstname, lastname, fullname, usn, branch, semester, section, cgpa
    usn = input("Enter the student's USN: ").upper()
    firstname = input("Enter the student's firstname: ").upper()
    lastname = input("Enter the student's lastname: ").upper()
    fullname = f"{firstname} {lastname}"
    branch = input("Enter the student's branch: ").upper()
    section = input("Enter the student's section: ").upper()
    semester = int(input("Enter the semester the student is in: "))
    cgpa = float(input("Enter the student's CGPA: "))


# Test table creation
# cursor.execute(create_table)

while True:
    # Get student info
    get_student_info()

    # Validate info and try adding an entry
    if validate_fields():
        cursor.execute(
            add_entry.format(
                usn, fullname, firstname, lastname, branch, semester, section, cgpa
            )
        )
    else:
        # Tell user and skip to the prompt
        print("Invalid information entered! Try again.")
        continue

    # Show table content
    print()
    print("#" * 20)
    cursor.execute(show_entries)
    entries = cursor.fetchall()
    print("student_data:")
    for entry in entries:
        print(entry)
    print("#" * 20)
    print()
