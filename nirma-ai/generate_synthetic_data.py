import csv
import os

data_dir = "synthetic_data"
os.makedirs(data_dir, exist_ok=True)

# 1. Campus Facilities
campus_data = [
    ["facility_id", "name", "category", "building", "location", "description", "working_hours", "contact"],
    ["F001", "Central Library", "Library", "Main Block", "Ground Floor", "University central library with 100k+ books", "8 AM - 8 PM", "library@nirma.edu"],
    ["F002", "AI Innovation Lab", "Laboratory", "CSE Block", "First Floor", "High-performance computing lab for AI/ML", "9 AM - 6 PM", "ailab@nirma.edu"],
    ["F003", "Sports Complex", "Sports", "Sports Wing", "Campus Rear", "Cricket, Basketball, and Indoor sports", "6 AM - 8 PM", "sports@nirma.edu"],
    ["F004", "Student Canteen", "Cafeteria", "Main Block", "Basement", "Multi-cuisine student food court", "8 AM - 7 PM", ""],
]
with open(f"{data_dir}/campus.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(campus_data)

# 2. Faculty
faculty_data = [
    ["faculty_id", "name", "department", "designation", "qualification", "specialization", "subjects", "email", "office", "profile_url"],
    ["FAC001", "Dr. Rajesh Shah", "CSE", "Professor", "PhD", "Machine Learning, Deep Learning", "ML, Neural Networks", "rajesh.shah@nirma.edu", "CSE-201", "https://nirma.edu/rajesh"],
    ["FAC002", "Dr. Smita Patel", "CSE", "Associate Professor", "PhD", "Data Science, NLP", "NLP, Python", "smita.patel@nirma.edu", "CSE-202", "https://nirma.edu/smita"],
    ["FAC003", "Prof. Anil Mehta", "IT", "Assistant Professor", "M.Tech", "Web Technologies", "Next.js, Fullstack", "anil.mehta@nirma.edu", "IT-105", ""],
]
with open(f"{data_dir}/faculty.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(faculty_data)

# 3. Syllabus
syllabus_data = [
    ["program", "department", "semester", "course_code", "course_name", "credits", "type", "description"],
    ["BTech", "CSE", "7", "CS701", "Machine Learning", "4", "Core", "Introduction to supervised and unsupervised machine learning algorithms."],
    ["BTech", "CSE", "7", "CS702", "Cloud Computing", "3", "Elective", "Cloud architecture, AWS, and deployment strategies."],
    ["BTech", "IT", "5", "IT501", "Web Development", "4", "Core", "Frontend and Backend web development using React and Node."],
]
with open(f"{data_dir}/courses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(syllabus_data)

# 4. Placements
placement_data = [
    ["company", "academic_year", "department", "role", "students_selected", "package", "package_type", "location", "eligibility", "source"],
    ["TCS", "2025-26", "CSE", "Software Engineer", "125", "7.5 LPA", "CTC", "Pune/Bangalore", "60% aggregate, no active backlogs", "Placement Report 2025-26"],
    ["Amazon", "2025-26", "CSE", "SDE-1", "8", "24 LPA", "CTC", "Bangalore", "75% aggregate, DSA round", "Placement Report 2025-26"],
    ["Infosys", "2025-26", "IT", "System Engineer", "90", "5.5 LPA", "CTC", "Pune", "60% aggregate", "Placement Report 2025-26"],
]
with open(f"{data_dir}/placements.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(placement_data)

# 5. FAQ
faq_data = [
    ["question", "answer", "category", "department", "source"],
    ["Where is the central library?", "The central library is located on the Ground Floor of the Main Block.", "Campus", "University", "Official Campus Info"],
    ["What is the highest placement package for CSE?", "According to the 2025-26 placement report, the highest package was 24 LPA offered by Amazon.", "Placements", "CSE", "Placement Report 2025-26"],
    ["Who teaches Machine Learning?", "Dr. Rajesh Shah teaches Machine Learning.", "Faculty", "CSE", "Faculty Directory"],
    ["What are the library timings?", "The library is open from 8 AM to 8 PM on working days.", "Campus", "University", "Library Rules"],
]
with open(f"{data_dir}/faq.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(faq_data)

print("Synthetic data generated successfully.")
