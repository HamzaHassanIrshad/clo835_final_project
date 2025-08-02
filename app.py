from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3

app = Flask(__name__)

# Load environment variables
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", "3306"))

BACKGROUND_IMAGE_URL = os.environ.get("BACKGROUND_IMAGE_URL", "")
MY_NAME = os.environ.get("MY_NAME", "CLO835 Student")

# Ensure static directory exists
if not os.path.exists("static"):
    os.makedirs("static")

# Download image from S3
def download_image():
    if not BACKGROUND_IMAGE_URL:
        print("No BACKGROUND_IMAGE_URL set")
        return
    try:
        s3 = boto3.client("s3")
        bucket_name = BACKGROUND_IMAGE_URL.split("/")[2].split(".")[0]
        key = "/".join(BACKGROUND_IMAGE_URL.split("/")[3:])
        s3.download_file(bucket_name, key, "static/bg.svg")
        print(f"Downloaded background image from: {BACKGROUND_IMAGE_URL}")
    except Exception as e:
        print(f"Error downloading image: {e}")

# Create a connection to the MySQL database
def get_db_connection():
    try:
        return connections.Connection(
            host=DBHOST,
            port=DBPORT,
            user=DBUSER,
            password=DBPWD,
            db=DATABASE
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Main Routes
@app.route("/", methods=["GET", "POST"])
def home():
    download_image()
    return render_template("addemp.html", bg_image="bg.svg", my_name=MY_NAME)

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", bg_image="bg.svg", my_name=MY_NAME)

@app.route("/addemp", methods=["POST"])
def AddEmp():
    emp_id = request.form["emp_id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    primary_skill = request.form["primary_skill"]
    location = request.form["location"]

    db_conn = get_db_connection()
    if not db_conn:
        return render_template("error.html", message="Database connection failed", bg_image="bg.svg", my_name=MY_NAME)

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
        print("Data inserted into DB.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        emp_name = "Error occurred"
    finally:
        cursor.close()
        db_conn.close()

    return render_template("addempoutput.html", name=emp_name, bg_image="bg.svg", my_name=MY_NAME)

@app.route("/getemp", methods=["GET", "POST"])
def GetEmp():
    return render_template("getemp.html", bg_image="bg.svg", my_name=MY_NAME)

@app.route("/fetchdata", methods=["GET", "POST"])
def FetchData():
    emp_id = request.form["emp_id"]
    output = {}
    
    db_conn = get_db_connection()
    if not db_conn:
        return render_template("error.html", message="Database connection failed", bg_image="bg.svg", my_name=MY_NAME)

    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()
    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        cursor.close()
        db_conn.close()

    return render_template("getempoutput.html", id=output.get("emp_id"), fname=output.get("first_name"),
                           lname=output.get("last_name"), interest=output.get("primary_skills"),
                           location=output.get("location"), bg_image="bg.svg", my_name=MY_NAME)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
