import requests
import sys
import pandas as pd
from enum import Enum

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
    
class Subject(Enum):
    STREAMING_DE_DONNEES = 'Streaming de données'
    SYSTEMES_DISTRIBUES = 'Systèmes distribués'
    AUTOMATION = 'Automation'
    CLASSIFICATION = 'Classification'
    MACHINE_LEARNING = 'Machine Learning'
    BDD = 'BDD'
    DOCKER = 'Docker'
    DATA_SCIENCE = 'Data Science'
    

endpoint = "http://127.0.0.1:8000/qcm/"

data = get_http_response(endpoint)

subjects = set()

for item in data:
    subjects.add(item['subject'])

subjects = list(subjects)

def get_data_by_subject(data, subject: str):
    if subject in [member.value for member in Subject]:
        filtered_data = [item for item in data if item['subject'] == subject]
        # return pd.DataFrame(filtered_data)
        return filtered_data
    else:
        raise ValueError("Invalid subject provided")

# Example usage:
subject_data = get_data_by_subject(data, 'Docker')
# subject_data_df = get_data_by_subject(data, 'Streaming de données')

data_df = pd.DataFrame(data)
subjects_df = pd.DataFrame({'subject': list(subjects)})

print(data_df.head())
print('\n')
print(subjects)
print('\n')
print(subjects_df)
print('\n')
print(Subject.AUTOMATION.value)
print('\n')
print(subject_data.__len__())
print('\n')
print(subject_data[:2])

# [
#   {
#     "id": 0,
#     "question": "Que signifie le sigle No-SQL ?",
#     "subject": "BDD",
#     "use": "Test de positionnement",
#     "correct": "A",
#     "responseA": "Pas seulement SQL",
#     "responseB": "Pas de SQL",
#     "responseC": "Pas tout SQL",
#     "responseD": "",
#     "remark": ""
#   },
#   {
#     "id": 1,
#     "question": "Cassandra et HBase sont des bases de données",
#     "subject": "BDD",
#     "use": "Test de positionnement",
#     "correct": "C",
#     "responseA": "relationnelles",
#     "responseB": "orientées objet",
#     "responseC": "orientées colonne",
#     "responseD": "orientées graphe",
#     "remark": ""
#   }
#   .
#   .
#   .
#   ]
