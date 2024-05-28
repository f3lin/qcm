import pandas as pd
from typing import List
from models import CSVQuestion


def load_csv(url: str,  destination: str):
    """
    Charge les données à partir de l'URL spécifiée et les enregistre dans le fichier de destination.
    
    Args:
        url (str): L'URL à partir de laquelle charger les données.
        destination (str): Le chemin du fichier de destination.
    """
    df = pd.read_csv(url)
    df['subject'] = df['subject'].replace({'Sytèmes distribués': 'Systèmes distribués'}) # Correction des erreurs de typographie
    df = df.dropna(subset=['correct'])  # Retire les lignes où 'correct' est NaN
    df = df[df['correct'] != ""]  # Retire les lignes où 'correct' est une chaîne de charactèr vide
    df = df.fillna('')  # Remplacer les NaN par des chaînes vides
    df.to_csv(destination, index=False)


def verify_data_existance(question: CSVQuestion, df: pd.DataFrame) -> bool:
    """
    Verifies if the provided question exists in the DataFrame.

    Args:
        question (CSVQuestion): The question to verify.
        df (pd.DataFrame): The DataFrame containing the questions.

    Returns:
        bool: True if the question exists, False otherwise.
    """
    # Vérifier si la question existe déjà dans les données
    if not df[(df['question'] == question.question) & (df['subject'] == question.subject)].empty:
        return True
    
    if question.correct=="":
        return True 
    
    return False

def verify_use_existance(use: str, df: pd.DataFrame) -> bool:
    """
    Verifies if the provided 'use' exists in the DataFrame.

    Args:
        use (str): The 'use' value to verify.
        df (pd.DataFrame): The DataFrame containing the questions.

    Returns:
        bool: True if the 'use' exists, False otherwise.
    """
    return True if use in df['use'].unique() else False

def verify_subject_existance(subjects: List[str], df: pd.DataFrame) -> bool:
    """
    Verifies if the provided subjects exist in the DataFrame.

    Args:
        subjects (List[str]): The list of subjects to verify.
        df (pd.DataFrame): The DataFrame containing the questions.

    Returns:
        bool: True if all subjects exist, False otherwise.
    """
    for subject in subjects:
        if subject not in df['subject'].unique():
            return False
    return True

def convert_df_to_CSVQuestion_List(df: pd.DataFrame):
    """
    Converts DataFrame rows to a list of CSVQuestion objects.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        List[CSVQuestion]: A list of CSVQuestion objects.
    """
    df_list = [CSVQuestion(**row) for row in df.to_dict(orient='records')]
    return df_list

def convert_CSVQuestion_List_to_dict_list(df_list: List[CSVQuestion]):
    """
    Converts a list of CSVQuestion objects to a list of dictionaries.

    Args:
        df_list (List[CSVQuestion]): The list of CSVQuestion objects.

    Returns:
        List[dict]: A list of dictionaries representing CSVQuestion objects.
    """
    return [q.model_dump() for q in df_list]

def get_questions(use: str, subjects: List[str], num_questions: int, df: pd.DataFrame) -> List[CSVQuestion]:
    """
    Retrieves a specified number of questions based on 'use' and subjects from the DataFrame.

    Args:
        use (str): The 'use' value to filter questions.
        subjects (List[str]): The list of subjects to filter questions.
        num_questions (int): The number of questions to retrieve.
        df (pd.DataFrame): The DataFrame containing the questions.

    Returns:
        List[CSVQuestion]: A list of CSVQuestion objects.
    """
    if not verify_use_existance(use, df):
        raise ValueError("The use you provide is not available. Availables Uses are: {uses}".format(uses=df['use'].unique()))
    elif not verify_subject_existance(subjects, df):
        raise ValueError("The subjects you provide are not available. Availables Subjects are: {subjects}".format(subjects=df['subject'].unique()))
    else:
        filtered_questions = df[(df['use'] == use) & (df['subject'].isin(subjects))]
        if len(filtered_questions) < num_questions:
            raise ValueError("Not enough questions available for the specified criteria. Number of questions available: {questions}".format(questions=len(filtered_questions)))
        
        filtered_questions = filtered_questions.sample(n=num_questions)
        filtered_questions_list = convert_df_to_CSVQuestion_List(filtered_questions)
        return filtered_questions_list

def add_question(question: CSVQuestion, df: pd.DataFrame, destination: str):
    """
    Adds a new question to the DataFrame and saves it to the destination file.

    Args:
        question (CSVQuestion): The question to add.
        df (pd.DataFrame): The DataFrame containing the questions.
        destination (str): The path to the destination file.
    """
    if not verify_data_existance(question, df):
        # Convert the new question to a dictionary and add it to the DataFrame
        new_row = pd.DataFrame([question.model_dump()])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(destination, index=False)
