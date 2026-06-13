print("SMART EVAL BACKEND LOADED")

# ============================================
# IMPORTS
# ============================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

import pymysql
import os
import fitz
import boto3

from PIL import Image

from google import genai

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# ============================================
# LOAD ENV
# ============================================

load_dotenv()

# ============================================
# FLASK SETUP
# ============================================

app = Flask(__name__)

CORS(app)

# ============================================
# MYSQL CONFIG
# ============================================

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT'))

# ============================================
# DATABASE CONNECTION
# ============================================

def get_db_connection():

    connection = pymysql.connect(

        host=os.getenv("DB_HOST"),

        user=os.getenv("DB_USER"),

        password=os.getenv("DB_PASSWORD"),

        database=os.getenv("DB_NAME"),

        port=int(os.getenv("DB_PORT")),

        cursorclass=pymysql.cursors.DictCursor
    )

    return connection

# ============================================
# GEMINI API
# ============================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ================= AWS S3 CONFIG =================

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
FACULTY_BUCKET = os.getenv("FACULTY_BUCKET")
STUDENT_BUCKET = os.getenv("STUDENT_BUCKET")

# ================= S3 CLIENT =================

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# ============================================
# FOLDERS
# ============================================

UPLOAD_FOLDER = "uploads"

ASSIGNMENT_FOLDER = "assignments"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(ASSIGNMENT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["ASSIGNMENT_FOLDER"] = ASSIGNMENT_FOLDER

# ============================================
# HOME ROUTE
# ============================================

@app.route("/")
def home():

    return jsonify({

        "status": "ok",

        "message": "SmartEval AI Backend is running"

    })

# ============================================
# TEST DATABASE
# ============================================

@app.route("/test-db")
def test_db():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE();")

        db_name = cursor.fetchone()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "database": db_name

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        })

# ============================================
# REGISTER STUDENT
# ============================================

@app.route("/register-student", methods=["POST"])
def register_student():

    try:

        data = request.json

        name = data.get("name")

        email = data.get("email")

        password = data.get("password")

        branch = data.get("branch")

        phone = data.get("phone")

        id_number = data.get("id_number")

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO users
        (
            name,
            email,
            password_hash,
            role,
            branch,
            phone,
            id_number
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (

            name,

            email,

            hashed_password,

            "student",

            branch,

            phone,

            id_number
        ))

        connection.commit()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "message": "Student Registered Successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# REGISTER FACULTY
# ============================================

@app.route("/register-faculty", methods=["POST"])
def register_faculty():

    try:

        data = request.json

        name = data.get("name")

        email = data.get("email")

        password = data.get("password")

        branch = data.get("branch")

        phone = data.get("phone")

        id_number = data.get("id_number")

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO users
        (
            name,
            email,
            password_hash,
            role,
            branch,
            phone,
            id_number
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (

            name,

            email,

            hashed_password,

            "faculty",

            branch,

            phone,

            id_number
        ))

        connection.commit()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "message": "Faculty Registered Successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# LOGIN
# ============================================

@app.route("/login", methods=["POST"])
def login():

    try:

        data = request.json

        email = data.get("email")

        password = data.get("password")

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        SELECT * FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        connection.close()

        if not user:

            return jsonify({

                "success": False,

                "message": "User Not Found"

            })

        if not check_password_hash(
            user["password_hash"],
            password
        ):

            return jsonify({

                "success": False,

                "message": "Invalid Password"

            })

        return jsonify({

            "success": True,

            "message": "Login Successful",

            "user": {

                "id": user["id"],

                "name": user["name"],

                "email": user["email"],

                "role": user["role"],

                "branch": user["branch"]

            }

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# CREATE ASSIGNMENT
# ============================================

@app.route("/create-assignment", methods=["POST"])
def create_assignment():

    try:

        faculty_id = request.form.get("faculty_id")

        title = request.form.get("title")

        description = request.form.get("description")

        deadline = request.form.get("deadline")

        difficulty = request.form.get("difficulty")

        pdf = request.files.get("pdf")

        if not pdf:

            return jsonify({

                "success": False,

                "message": "No PDF Uploaded"

            })

        filename = pdf.filename

        # Upload faculty PDF to S3
        s3.upload_fileobj(
            pdf,
            FACULTY_BUCKET,
            filename
        )

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO assignments
        (
            faculty_id,
            title,
            description,
            deadline,
            difficulty,
            assignment_pdf_url,
            assignment_s3_key
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (

            faculty_id,

            title,

            description,

            deadline,

            difficulty,

            filename,

            filename
        ))

        connection.commit()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "message": "Assignment Created Successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# GET ASSIGNMENTS
# ============================================

@app.route("/get-assignments")
def get_assignments():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            assignments.id,
            assignments.title,
            assignments.description,
            assignments.deadline,
            assignments.difficulty,
            assignments.assignment_pdf_url,
            users.name AS faculty_name
        FROM assignments

        JOIN users
        ON assignments.faculty_id = users.id

        ORDER BY assignments.created_at DESC
        """

        cursor.execute(query)

        assignments = cursor.fetchall()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "assignments": assignments

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# PDF TO IMAGE
# ============================================

def convert_pdf_to_images(pdf_path):

    image_paths = []

    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):

        page = pdf_document[page_number]

        pix = page.get_pixmap()

        image_path = os.path.join(

            UPLOAD_FOLDER,

            f"page_{page_number + 1}.png"
        )

        if os.path.exists(image_path):

            os.remove(image_path)

        pix.save(image_path)

        image_paths.append(image_path)

    return image_paths

# ============================================
# UPLOAD SUBMISSION
# ============================================

@app.route("/upload-submission", methods=["POST"])
def upload_submission():

    try:

        assignment_id = request.form.get("assignment_id")

        student_id = request.form.get("student_id")

        file = request.files.get("pdf")

        if not file:

            return jsonify({

                "success": False,

                "message": "No PDF Uploaded"

            })

        filename = file.filename

        pdf_path = os.path.join(

            app.config["UPLOAD_FOLDER"],

            filename
        )

        # Save temporarily
        file.save(pdf_path)

        # Upload student PDF to S3
        with open(pdf_path, "rb") as pdf_file:
            s3.upload_fileobj(
                pdf_file,
                STUDENT_BUCKET,
                filename
            )

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        INSERT INTO submissions
        (
            assignment_id,
            student_id,
            submission_pdf_url,
            submission_s3_key
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (

            assignment_id,

            student_id,

            filename,

            filename
        ))

        submission_id = cursor.lastrowid

        connection.commit()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "message": "Submission Uploaded Successfully",

            "submission_id": submission_id

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# EVALUATE SUBMISSION
# ============================================

@app.route("/evaluate-submission/<int:submission_id>")
def evaluate_submission(submission_id):

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        SELECT * FROM submissions
        WHERE id = %s
        """

        cursor.execute(query, (submission_id,))

        submission = cursor.fetchone()

        if not submission:

            return jsonify({

                "success": False,

                "message": "Submission Not Found"

            })

        pdf_path = os.path.join(

            app.config["UPLOAD_FOLDER"],

            submission["submission_pdf_url"]
        )

        image_paths = convert_pdf_to_images(pdf_path)

        images = []

        for image_path in image_paths:

            image = Image.open(image_path)

            images.append(image)

        prompt = """

You are SmartEval AI.

Analyze this assignment carefully.

Evaluate based on:

1. Accuracy
2. Completeness
3. Technical Understanding
4. AWS Concepts
5. Screenshots & Proof

Give:

- Score out of 100
- Strengths
- Weaknesses
- Missing Concepts
- Final Feedback

"""

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=[prompt] + images
        )

        evaluation_text = response.text

        score = 85

        query = """
        INSERT INTO evaluation_results
        (
            submission_id,
            ai_model,
            score,
            strengths,
            weaknesses,
            missing_points,
            feedback,
            ai_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (

            submission_id,

            "gemini-2.5-flash",

            score,

            "Good Technical Understanding",

            "Needs Better Documentation",

            "Missing AWS Architecture Explanation",

            evaluation_text,

            "success"
        ))

        update_query = """
        UPDATE submissions
        SET submission_status = 'completed'
        WHERE id = %s
        """

        cursor.execute(update_query, (submission_id,))

        connection.commit()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "evaluation": evaluation_text

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# GET SUBMISSIONS
# ============================================

@app.route("/get-submissions")
def get_submissions():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        query = """
        SELECT
            submissions.id,
            submissions.submission_status,
            submissions.submitted_at,

            users.name AS student_name,

            assignments.title AS assignment_title

        FROM submissions

        JOIN users
        ON submissions.student_id = users.id

        JOIN assignments
        ON submissions.assignment_id = assignments.id

        ORDER BY submissions.submitted_at DESC
        """

        cursor.execute(query)

        submissions = cursor.fetchall()

        cursor.close()

        connection.close()

        return jsonify({

            "success": True,

            "submissions": submissions

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })

# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":

    print("\n==================================================")

    print("  SmartEval AI Backend")

    print("  http://127.0.0.1:5000")

    print("==================================================\n")

    app.run(debug=True)