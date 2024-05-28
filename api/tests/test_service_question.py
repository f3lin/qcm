import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from service.question import find_questions, create_question, get_subjects, get_uses, load_dataframe
from models import CSVQuestion

# Get the directory path of the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the CSV file
CSV_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'data.csv')

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame([
        {
            'question': 'Sample Question 1',
            'subject': 'Subject 1',
            'use': 'Sample Use',
            'correct': 'Answer 1',
            'responseA': 'A1',
            'responseB': 'A2',
            'responseC': 'A3',
            'responseD': 'A4',
            'remark': ''
        },
        {
            'question': 'Sample Question 2',
            'subject': 'Subject 1',
            'use': 'Sample Use',
            'correct': 'Answer 2',
            'responseA': 'B1',
            'responseB': 'B2',
            'responseC': 'B3',
            'responseD': 'B4',
            'remark': ''
        }
    ])

def test_load_dataframe(sample_dataframe):
    with patch('pandas.read_csv', return_value=sample_dataframe):
        df = load_dataframe(CSV_FILE_PATH)
        pd.testing.assert_frame_equal(df, sample_dataframe)

@patch('service.question.load_dataframe')
def test_find_questions(mock_load_dataframe, sample_dataframe):
    mock_load_dataframe.return_value = sample_dataframe
    questions = find_questions('Sample Use', ['Subject 1'], 1)
    assert len(questions) == 1
    assert questions[0].question in ['Sample Question 1', 'Sample Question 2']

@patch('service.question.load_dataframe')
def test_create_question(mock_load_dataframe, sample_dataframe):
    mock_load_dataframe.return_value = sample_dataframe
    new_question = CSVQuestion(
        question='New Question',
        subject='New Subject',
        use='Sample Use',
        correct='New Answer',
        responseA='A1',
        responseB='A2',
        responseC='A3',
        responseD='A4',
        remark=''
    )

    # Successful case
    with patch('service.question.add_question'):
        result = create_question(new_question)
        assert result == new_question

    # Failure case: duplicate question
    with patch('csv_management.verify_question_subject_and_subject_existence', return_value=True):
        with pytest.raises(ValueError, match="Question already exists"):
            create_question(new_question)

    # Failure case: empty 'correct' field
    invalid_question = CSVQuestion(
        question='Invalid Question',
        subject='New Subject',
        use='Sample Use',
        correct='',
        responseA='A1',
        responseB='A2',
        responseC='A3',
        responseD='A4',
        remark=''
    )
    with pytest.raises(ValueError, match="Question correct answer can't be empty"):
        create_question(invalid_question)

@patch('service.question.load_dataframe')
def test_get_subjects(mock_load_dataframe, sample_dataframe):
    mock_load_dataframe.return_value = sample_dataframe
    subjects = get_subjects()
    assert subjects == ['Subject 1']

@patch('service.question.load_dataframe')
def test_get_uses(mock_load_dataframe, sample_dataframe):
    mock_load_dataframe.return_value = sample_dataframe
    uses = get_uses()
    assert uses == ['Sample Use']
