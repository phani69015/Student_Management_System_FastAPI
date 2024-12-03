import requests

BASE_URL = "http://127.0.0.1:8000"  
def test_create_student():
    payload = {
        "name": "Test User",
        "age": 20,
        "address": {"country": "India", "city": "Delhi"}
    }
    response = requests.post(f"{BASE_URL}/students", json=payload)
    print("Create Student:", response.status_code, response.json())

def test_list_students():
    response = requests.get(f"{BASE_URL}/students")
    print("List Students:", response.status_code, response.json())

def test_fetch_student(student_id):
    response = requests.get(f"{BASE_URL}/students/{student_id}")
    print("Fetch Student:", response.status_code, response.json())

def test_update_student(student_id):
    payload = {"age": 25}
    response = requests.patch(f"{BASE_URL}/students/{student_id}", json=payload)
    print("Update Student:", response.status_code)
    if response.status_code == 204:
        print("Student updated successfully.")

def test_delete_student(student_id):
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    print("Delete Student:", response.status_code)
    if response.status_code == 200:
        print("Student deleted successfully.")

if __name__ == "__main__":
    create_response = requests.post(
        f"{BASE_URL}/students",
        json={
            "name": "Test User",
            "age": 20,
            "address": {"country": "India", "city": "Delhi"}
        },
    )
    print("Create Student:", create_response.status_code, create_response.json())

    student_id = '674f403bad07006119ccd4ae'
    if student_id:
        test_fetch_student(student_id)

        test_update_student(student_id)

        test_list_students()

        test_delete_student(student_id)
