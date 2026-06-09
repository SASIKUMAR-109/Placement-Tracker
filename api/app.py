# TODO: Add PDF scraper for company-level data
# Source: https://www.nirfindia.org/nirfpdfcdn/YEAR/pdf/Overall/INSTITUTE_ID.pdf
# Library needed: pdfplumber
# Tables needed: companies, placement_records

from flask import Flask, jsonify, request
from flask_cors import CORS 
import sqlite3
import os


def get_db():
    path = os.path.dirname(r"C:\Users\DELL 3400\OneDrive\Desktop\placement_tracker\api\app.py")
    path = os.path.dirname(path)
    path = os.path.join(path, 'database', 'placement.db')
    conn = sqlite3.connect(path)
    return conn


app = Flask(__name__)

CORS(app) 


@app.route("/")
def object_Return():
    return jsonify({"status":"api is running"})

@app.route("/api/colleges")
def get_colleges():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT college_id, college_name ,city , state, college_type  FROM colleges")
    colleges = cursor.fetchall()
    college_list = []
    for i in colleges:
        college_dict = {
            "college_id": i[0],
            "college_name":i[1],
            "city": i [2],
            "state": i[3],
            "college_type": i[4]
        }
        college_list.append(college_dict)
    conn.close()
    return jsonify(college_list)

@app.route("/api/college")
def get_college_by_id():
    name = request.args.get('name')
    if name == None or name =="":
        return jsonify({"error":"College name is required"}),400
    else:
        conn = get_db()
        cursor = conn.cursor()
        select_query_1 = "SELECT college_id, college_name, city, state, college_type FROM colleges where college_name LIKE ? "
        cursor.execute(select_query_1, ('%' + name + '%',))
        result = cursor.fetchone()
    
        if result is None:
            conn.close()
            return jsonify({"error":"College not found"}),404
        else:
            college_dict = {
                "college_id": result[0],
                "college_name" : result[1],
                "city":result[2],
                "state" : result[3],
                "college_type" : result[4]
            } 
            
            select_query_2 = "SELECT year,branch , total_students , students_placed, placement_pct ,median_package_lpa FROM placement_summary WHERE college_id = ? ORDER BY year"
            cursor.execute(select_query_2, (result[0],))
            result_2 = cursor.fetchall()
            placement_summary_list = []
            for i in result_2:
                placement_summary_dict = {
                    "year": i[0],
                    "branch": i[1],
                    "total_students": i[2],
                    "students_placed": i[3],
                    "placement_pct": i[4],
                    "median_package_lpa": i[5]
                }
                placement_summary_list.append(placement_summary_dict)
            conn.close()    
            return jsonify ({"college":college_dict, "placements":placement_summary_list})
        
if __name__ == "__main__":
    app.run(debug = True)