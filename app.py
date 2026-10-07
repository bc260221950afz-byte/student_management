import streamlit as st
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]
students = db["students"]
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓"
)
st.title("🎓 Student Management System")
st.write("Manage students using MongoDB + Streamlit")
name = st.text_input("Student Name")
age = st.number_input(
    "Age",
    min_value=1,
    max_value=100,
    value=18
)
course = st.selectbox(
    "Course",
    ["AI", "Machine Learning", "Data Science"]
)
marks = st.number_input(
    "Marks",
    min_value=0,
    max_value=100,
    value=0
)
if st.button("Add Student"):
    if name.strip() == "":
        st.warning("Please enter student name.")
    else:
        student = {
            "name": name,
            "age": age,
            "course": course,
            "marks": marks
        }
        students.insert_one(student)
        st.success("Student added successfully!")
all_students = students.find()
student_list = []
for student in all_students:
    student_list.append({
        "ID": str(student["_id"]),
        "Name": student["name"],
        "Age": student["age"],
        "Course": student["course"],
        "Marks": student["marks"]
    })
if len(student_list) > 0:
    st.dataframe(
        student_list,
        use_container_width=True
    )
else:
    st.info("No students found.")
update_name = st.text_input("Enter student name to update")
new_marks = st.number_input(
    "New Marks",
    min_value=0,
    max_value=100,
    value=0
)
if st.button("Update Marks"):
    result = students.update_one(
        {"name": update_name},
        {"$set": {"marks": new_marks}}
    )
    if result.matched_count > 0:
        st.success("Student updated successfully!")
    else:
        st.warning("Student not found.")
delete_name = st.text_input("Enter student name to delete")
if st.button("Delete Student"):
    result = students.delete_one(
        {"name": delete_name}
    )
    if result.deleted_count > 0:
        st.success("Student deleted successfully!")
    else:
        st.warning("Student not found.")