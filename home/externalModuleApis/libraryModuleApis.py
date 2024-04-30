import http.client
import json

def create_library_account(student_id):
    try:
        conn = http.client.HTTPConnection("localhost", 80)
        payload = json.dumps({
            "studentId": student_id
        })
        headers = {
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/api/register", payload, headers)
        response = conn.getresponse()
        if response.status == 200:
            return True
        else:
            print(f"Failed to create library account. Status code: {response.status}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
