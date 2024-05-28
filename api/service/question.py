import os
import pandas as pd
from typing import List
from models import CSVQuestion
from csv_management import get_questions, add_question, remove_question

# Get the directory path of the current file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the CSV file
CSV_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'data', 'data.csv')

# df = pd.read_csv(CSV_FILE_PATH)

def load_dataframe(CSV_FILE_PATH:str):
    return pd.read_csv(CSV_FILE_PATH)
    
def find_questions(use: str, subjects: List[str], num_questions: int) -> List[CSVQuestion]:
    """
    Retrieves questions from the CSV file.

    Returns:
        List[CSVQuestion]: A list of CSVQuestion objects representing the questions.
    """
    # Read questions from the CSV file
    df = load_dataframe(CSV_FILE_PATH)
    return get_questions(use, subjects, num_questions, pd.DataFrame(df))

def create_question(question: CSVQuestion) -> CSVQuestion:
    """
    Adds a new question to the CSV file.

    Args:
        question (CSVQuestion): The new question to add.

    Returns:
        CSVQuestion: The added question.
    """
    df = load_dataframe(CSV_FILE_PATH)
    add_question(question, df, CSV_FILE_PATH)
    return question

# TODO: should be tested
def delete_question(question: CSVQuestion) -> bool:
    """
    Deletes a question from the CSV file.

    Args:
        question (CSVQuestion): The question to delete.

    Returns:
        CSVQuestion: The deleted question.
    """
    df = load_dataframe(CSV_FILE_PATH)

    if remove_question(question, df, CSV_FILE_PATH):
        return True
    else:
        return False

def get_subjects() -> List[str]:
    """
    Retrieves unique subjects from the CSV file.

    Returns:
        List[str]: A list of unique subjects.
    """
    df = load_dataframe(CSV_FILE_PATH)
    return df['subject'].unique().tolist()

def get_uses() -> List[str]:
    """
    Retrieves unique uses from the CSV file.

    Returns:
        List[str]: A list of unique uses.
    """
    df = load_dataframe(CSV_FILE_PATH)
    return df['use'].unique().tolist()