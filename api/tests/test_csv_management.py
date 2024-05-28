import pandas as pd
import pytest
from csv_management import (
    add_question, 
    convert_CSVQuestion_List_to_dict_list,
    convert_df_to_CSVQuestion_List, 
    get_questions, load_csv, 
    verify_data_existance, 
    verify_subject_existance,
    verify_use_existance
)

from models import CSVQuestion


@pytest.fixture
def sample_df():
    return pd.DataFrame([
        {
            'question': 'Question 1',
            'subject': 'Subject 1',
            'use': 'Exam',
            'correct': 'Answer 1',
            'responseA': 'A1',
            'responseB': 'A2',
            'responseC': 'A3',
            'responseD': 'A4',
            'remark': ''
        },
        {
            'question': 'Question 2',
            'subject': 'Subject 2',
            'use': 'Quiz',
            'correct': 'Answer 2',
            'responseA': 'B1',
            'responseB': 'B2',
            'responseC': 'B3',
            'responseD': 'B4',
            'remark': ''
        }
    ])

def test_load_csv(tmp_path, sample_df):
    # Sauvegarder les données de test dans un fichier CSV temporaire
    test_csv_path = tmp_path / "test.csv"
    sample_df.to_csv(test_csv_path, index=False)

    # Load the CSV file and check if the loaded data is equal to the sample data
    load_csv(test_csv_path, tmp_path / "loaded_test.csv")
    loaded_data = pd.read_csv(tmp_path / "loaded_test.csv").fillna('')    
    assert loaded_data.equals(sample_df.fillna(''))

def test_verify_data_existance(sample_df):
    # Create a CSVQuestion object for testing
    question = CSVQuestion(
        question='Question 1',
        subject='Subject 1',
        use='Exam',
        correct='Answer 1',
        responseA='A1',
        responseB='A2',
        responseC='A3',
        responseD='A4',
        remark=''
    )
    
    # Ensure the question exists in the DataFrame
    assert verify_data_existance(question, sample_df) == True
    
    # Ensure a non-existent question returns False
    non_existent_question = CSVQuestion(
        question='Non-existent Question',
        subject='Subject 1',
        use='Exam',
        correct='Answer 1',
        responseA='A1',
        responseB='A2',
        responseC='A3',
        responseD='A4',
        remark=''
    )
    assert verify_data_existance(non_existent_question, sample_df) == False

def test_verify_use_existance(sample_df):
    # Ensure existing 'use' returns True
    assert verify_use_existance('Exam', sample_df) == True
    
    # Ensure non-existent 'use' returns False
    assert verify_use_existance('Non-existent Use', sample_df) == False

def test_verify_subject_existance(sample_df):
    # Ensure existing subjects return True
    assert verify_subject_existance(['Subject 1', 'Subject 2'], sample_df) == True
    
    # Ensure non-existent subject returns False
    assert verify_subject_existance(['Non-existent Subject'], sample_df) == False

def test_convert_df_to_CSVQuestion_List(sample_df):
    # Convert DataFrame to a list of CSVQuestion objects
    question_list = convert_df_to_CSVQuestion_List(sample_df)
    
    # Ensure the length of the list matches the DataFrame rows
    assert len(question_list) == len(sample_df)
    
    # Ensure each element in the list is a CSVQuestion object
    assert all(isinstance(q, CSVQuestion) for q in question_list)

def test_convert_CSVQuestion_List_to_dict_list(sample_df):
    # Convert CSVQuestion list to a list of dictionaries
    question_list = convert_df_to_CSVQuestion_List(sample_df)
    dict_list = convert_CSVQuestion_List_to_dict_list(question_list)
    
    # Ensure the length of the list matches the length of the CSVQuestion list
    assert len(dict_list) == len(question_list)
    
    # Ensure each element in the list is a dictionary
    assert all(isinstance(d, dict) for d in dict_list)

def test_get_questions(sample_df):
    # Ensure existing 'use' and subjects return a list of questions
    questions = get_questions('Exam', ['Subject 1'], 1, sample_df)
    assert len(questions) == 1
    assert isinstance(questions[0], CSVQuestion)
    
    # Ensure non-existent 'use' raises a ValueError
    with pytest.raises(ValueError):
        get_questions('Non-existent Use', ['Subject 1'], 1, sample_df)
    
    # Ensure non-existent subjects raise a ValueError
    with pytest.raises(ValueError):
        get_questions('Exam', ['Non-existent Subject'], 1, sample_df)

def test_add_question(tmp_path, sample_df):
    # Create a new question to add
    new_question = CSVQuestion(
        question='New Question',
        subject='New Subject',
        use='New Use',
        correct='New Answer',
        responseA='A1',
        responseB='A2',
        responseC='A3',
        responseD='A4',
        remark=None
    )
    
    # Add the new question to the DataFrame and check if it's present
    add_question(new_question, sample_df, tmp_path / "updated_test.csv")
    updated_data = pd.read_csv(tmp_path / "updated_test.csv")
    assert verify_data_existance(new_question, updated_data) == True