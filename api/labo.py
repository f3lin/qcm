import requests
import sys

def get_http_response(endpoint) :
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()
    elif 400 <= response.status_code <= 499:
        sys.exit("Client Error.")
    elif 500 <= response.status_code <= 599:
        sys.exit("Server Error.")
    else:
        return None

endpoint = "http://127.0.0.1:8000/qcm/"

data = get_http_response(endpoint)

subjects = set()

for item in data:
    subjects.add(item['subject'])


def get_question_by_subject(data, subject: str):
    if subject in subjects:
        filtered_question = [question for question in data if question['subject'] == subject]
        return filtered_question
    else:
        raise ValueError("Invalid subject provided")

# Example usage:
filtered_question = get_question_by_subject(data, 'Docker')

print(data[:5])
print('\n')
print(filtered_question)
