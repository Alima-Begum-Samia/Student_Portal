import requests

def register_finance_account(student):
    try:
        data = {"studentId": student.user_id}
        url = 'http://localhost:8081/accounts/'
        response = requests.post(url, json=data)
        if response.status_code == 201:
            student.is_student = True
            student.save()
            return True
        else:
            print(f"Failed to create finance account. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False



def create_new_invoice(amount, due_date, invoice_type, student_id):
    data = {
        "amount": amount,
        "dueDate": due_date,
        "type": invoice_type,
        "account": {
            "studentId": student_id
        }
    }

    url = "http://localhost:8081/invoices/"
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            invoice_data = response.json()
            return {
                "is_created": True,
                "reference": invoice_data.get('reference', None)
            }
        elif response.status_code == 422:
            return {
                "is_created": False,
                "invalid_student": True
            }
        else:
            return {
                "is_created": False,
            }
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {
            "is_created": False,
        }


def cancel_invoice(reference):
    url = f"http://localhost:8081/invoices/{reference}/cancel"
    try:
        response = requests.delete(url)
        
        switch = {
            200: {'status': 200, 'message': 'Invoice Cancelled'},
            405: {'status': 405, 'message': "You can't Cancel an Invoice that is Already Paid."},
            404: {'status': 404, 'message': "Invoice not found"},
            400: {'status': 400, 'message': "Something Went Wrong. Please Ensure that Finance Module is Running."}
        }
        
        return switch.get(response.status_code)
    except Exception as e:
        return {'status': 400, "message": "Something Went Wrong. Please Ensure that Finance Module is Running."}
    

def get_student_invoices(user_id):
    url = f"http://localhost:8081/invoices"
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            all_invoices = response.json()
            invoices = [invoice for invoice in all_invoices.get("_embedded", {}).get("invoiceList", []) if invoice.get("studentId") == user_id]
            return invoices
        else:
            print(f"Failed to retrieve invoices. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_student_info(student_id):
    url = f"http://localhost:8081/accounts/student/{student_id}"
    
    try:
        response = requests.get(url)
        
        switch = {
            200: lambda account_info: {'hasAccount': True, 'hasOutstandingBalance': account_info.get('hasOutstandingBalance', False), 'error': False},
            404: lambda _: {'hasAccount': False, 'error': False},
            'default': lambda _: {'error': "Something Went Wrong!"}
        }
        
        return switch.get(response.status_code, switch['default'])(response.json() if response.status_code == 200 else None)
    
    except requests.RequestException as e:
        return {'error': "Unable to Send Request. Please ensure Finance Module is Running"}

