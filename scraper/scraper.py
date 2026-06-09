#step1 : read csv file rows one by one
#step2 : check if placement_column3 and placement_column4 are zero skip that row
#step3 : check if this college already exists in the DB using Institute_ID.
#step4 : If not, insert into colleges table and get the new ID. If yes, just get the existing ID.
#step5 :  Calculate total_students, placement_pct, and package_lpa. Fifth — Insert into placement_summary.
import csv
import os
import sqlite3
from datetime import datetime

db_path = os.path.dirname(r"C:\Users\DELL 3400\OneDrive\Desktop\placement_tracker\scraper\scraper.py")
db_path = os.path.dirname(db_path)
db_path =os.path.join(db_path, 'database', 'placement.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

government_keywords = [
    "Indian Institute of Technology",
    "National Institute of Technology",
    "Indian Institute of Management",
    "Indian Institute of Information Technology",
    "Indian Institute of Science",
    "Indian Institute of Science Education & Research",
    "All India Institute of Medical Sciences",
    "National Institute of Pharmaceutical Education and Research",
    "Jawaharlal Nehru University",
    "Banaras Hindu University",
    "Jamia Millia Islamia",
    "Aligarh Muslim University",
    "University of Delhi",
    "University of Hyderabad",
    "Anna University",
    "Jadavpur University",
    "Calcutta University",
    "Savitribai Phule Pune University",
    "Panjab University",
    "Osmania University",
    "Indian Agricultural Research Institute",
    "Visva Bharati",
    "Tamil Nadu Agricultural University"
]

private_keywords = [
    "Amity University",
    "Vellore Institute of Technology",
    "Birla Institute of Technology",
    "SRM Institute of Science and Technology",
    "Kalinga Institute of Industrial Technology",
    "Thapar Institute of Engineering and Technology",
    "Manipal Academy of Higher Education",
    "Amrita Vishwa Vidyapeetham",
    "Sathyabama Institute of Science and Technology",
    "Saveetha Institute of Medical and Technical Sciences",
    "Siksha",
    "Shiv Nadar University",
    "Symbiosis International",
    "JSS Academy of Higher Education and Research",
    "Narsee Monjee ",
    "Dr. D. Y. Patil Vidyapeeth",
    "Lovely Professional University",
    "Karunya Institute of Technology and Sciences",
    "B.S. Abdur Rahman Institute of Science and Technology",
    "Shanmugha Arts Science Technology & Research Academy"
]

path = r"C:\Users\DELL 3400\OneDrive\Desktop\placement_tracker\database\nirf_full_dataset_2017_2025.csv"
with open(path, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if (row['Placement_Col_3']=='0' or row['Placement_Col_3']=="") and (row['Placement_Col_4']=='0' or row['Placement_Col_4']==""):
            continue
        
        institute_id = row['Institute_ID']
        college_name = row['Name']
        city = row['City']
        state = row['State']
        select_query = "SELECT college_id FROM colleges WHERE college_name = ?"
        cursor.execute(select_query, (college_name,))
        result = cursor.fetchone()
        if result is None:
            if any(keyword in college_name for keyword in government_keywords):
                category = "Government"
            elif any(keyword in college_name for keyword in private_keywords):
                category = "Private"
            else:
                category = "Unknown"

            insert_query = "INSERT INTO colleges(college_name,city,state,college_type,institute_id,scraped_at) VALUES (?, ?, ?, ?, ?,?)"
            cursor.execute(insert_query,(college_name,city,state,category,institute_id,datetime.now()))
            college_id = cursor.lastrowid
        else:
            college_id = result[0]
        year = int(row['Ranking_Year'])
        if year ==2017:
            branch = row['Placement_Col_2'].strip()
            students_placed = row['Placement_Col_3']
            higher_studies_students = row['Placement_Col_4']
            package_lpa = row['Placement_Col_5']
            total_students = 0

            if (students_placed or  higher_studies_students):
                if students_placed.isdigit():
                    students_placed = int(students_placed)
                else:
                    students_placed = 0
                if higher_studies_students.isdigit():
                    higher_studies_students = int(higher_studies_students)
                else:
                    higher_studies_students = 0
                total_students = students_placed + higher_studies_students


            if total_students > 0:
                    placement_pct = (students_placed / total_students) * 100
            else:
                    placement_pct = 0.0
            
            if package_lpa.isdigit():
                if int(package_lpa) >10000:
                    package_lpa = round((int(package_lpa)/100000),2)
                else:
                    package_lpa=None
            else:
                package_lpa = None
        else:
            branch = row['Ranking_Year'] + '_' + row['Placement_Col_4'].strip()
            students_placed = row['Placement_Col_3']
            total_students = row['Placement_Col_2']
            if total_students.isdigit():
                total_students = int(total_students)
            else:
                total_students = 0
            if students_placed.isdigit():
                students_placed = int(students_placed)  
            else:                
                students_placed = 0
            
            if total_students > 0:
                placement_pct = (students_placed / total_students) * 100
            else:
                placement_pct = 0.0
            package_lpa = row['Placement_Col_9'].strip()
            if package_lpa == "":
                package_lpa = None
            else:
                package_lpa = package_lpa.split('(')[0].strip()
            if package_lpa is not None:
                if package_lpa.isdigit():
                    if int(package_lpa) >10000:
                        package_lpa = round((int(package_lpa)/100000),2)
                    else:
                        package_lpa=None
                

        
        check_query = "SELECT summary_id FROM placement_summary WHERE college_id = ? AND year = ? AND branch = ?"
        cursor.execute(check_query, (college_id, year, branch))
        result = cursor.fetchone()

        if result is None:
            insert_placement_query = "INSERT INTO placement_summary(college_id, year, branch, total_students, students_placed, placement_pct ,scraped_at,median_package_lpa) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_placement_query, (college_id, year, branch, total_students, students_placed, placement_pct, datetime.now(), package_lpa))
        else:
            update_query = "UPDATE placement_summary SET total_students = ?, students_placed = ?, placement_pct = ?, median_package_lpa = ?, scraped_at = ? WHERE summary_id = ?"
            cursor.execute(update_query, (total_students, students_placed, placement_pct, package_lpa, datetime.now(), result[0]))

    conn.commit()
    conn.close()