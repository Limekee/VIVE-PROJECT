
from typing import Tuple
import random
import string
import re
from collections import Counter
from string import *
from math import log
PASSWORD_CRITERIA = {
    # Length-related issues
    'TOO_SHORT': {
        'score': -30,
        'message': 'Password is too short (minimum 8 characters required)',
        'example': 'pass'
    },
    'RECOMMENDED_LONGER': {
        'score': -5,
        'message': 'Password could be stronger with at least 12 characters',
        'example': 'Password10!'
    },

    # Character composition
    'NO_UPPERCASE': {
        'score': -10,
        'message': 'Missing uppercase letters',
        'example': 'password123!'
    },
    'NO_LOWERCASE': {
        'score': -10,
        'message': 'Missing lowercase letters',
        'example': 'PASSWORD123!'
    },
    'NO_NUMBERS': {
        'score': -10,
        'message': 'Missing numbers',
        'example': 'Password!'
    },
    'NO_SPECIAL': {
        'score': -10,
        'message': 'Missing special characters',
        'example': 'Password123'
    },

    # Patterns and sequences
    'KEYBOARD_PATTERN': {
        'score': -20,
        'message': 'Contains keyboard pattern (e.g., qwerty, asdf)',
        'example': 'qwerty123'
    },
    'NUMERICAL_SEQUENCE': {
        'score': -15,
        'message': 'Contains simple number sequence (e.g., 123, 987)',
        'example': 'Password123'
    },
    'ALPHABETICAL_SEQUENCE': {
        'score': -15,
        'message': 'Contains alphabetical sequence (e.g., abc, xyz)',
        'example': 'Passwordabc!'
    },
    'REPEATED_CHARS': {
        'score': -15,
        'message': 'Contains repeated characters (e.g., aaa, 111)',
        'example': 'Password111!'
    },
    # Common substitutions
    'PREDICTABLE_SUBSTITUTIONS': {
        'score': -5,
        'message': 'Uses common character substitutions (e.g., a->@, i->1)',
        'example': 'P@ssw0rd'
    },

    # Structure
    'ONLY_LETTERS': {
        'score': -20,
        'message': 'Contains only letters',
        'example': 'Password'
    },
    'ONLY_NUMBERS': {
        'score': -25,
        'message': 'Contains only numbers',
        'example': '12345678'
    },
    'COMMON_STRUCTURE': {
        'score': -10,
        'message': 'Uses common password structure (e.g., Capitalize1!)',
        'example': 'Password1!'
    },

    # Context and dictionary
    'COMMON_PASSWORD': {
        'score': -50,
        'message': 'Matches commonly used password',
        'example': 'admin'
    },
    'COMMON_WORD': {
        'score': -20,
        'message': 'Contains common dictionary word',
        'example': 'monkey123'
    },
    'YEAR_PATTERN': {
        'score': -15,
        'message': 'Contains year-like pattern',
        'example': 'Password1990!'
    },

    # Entropy
    'LOW_ENTROPY': {
        'score': -15,
        'message': 'Low character diversity',
        'example': 'aaaaaa123'
    },

    # Positive criteria
    'GOOD_LENGTH': {
        'score': 20,
        'message': 'Good password length',
        'example': 'ThisIsALongPassword123!'
    },
    'STRONG_VARIETY': {
        'score': 20,
        'message': 'Good character variety',
        'example': 'P@ssw0rd$123'
    },
    'HIGH_ENTROPY': {
        'score': 20,
        'message': 'High character diversity',
        'example': 'P@s$w0rd#123'
    }
}
pop_eng_word=['admin', 'DragonPass', 'monkey', 'password','that', 'with', 'said', 'they', 'this', 'have', 'there', 'what', 'from', 'were', 'would', 'like', 'when', 'could', 'then', 'them', 'been', 'look', 'back', 'your', 'which', 'about', 'time', 'down', 'into', 'know', 'just', 'their', 'over', 'more', 'some', 'come', 'other', 'little', 'here', 'thing', 'hand', 'will', 'again', 'right', 'only', 'think', 'good', 'well', 'thought', 'than']
com_eng_word = ['admin', 'DragonPass', 'monkey', 'password', '123456', 'qwerty', 'abcdef', 'letmein', 'welcome', 'monkey', 'sunshine', 'iloveyou', 'admin', '123456789', 'trustno1', '12345678', '123123', 'password1']

def detect_patterns(password: str) -> list[str]:
    lower_password=password.lower()
    end_list_of_det_pat=[]

    list_of_keyboard_pattern='qwertyuiopasdfghjklzxcvbnm'
    only_aplh_password = ''.join(i if i  in ascii_lowercase else ' ' for i in lower_password).split()
    if any(i in list_of_keyboard_pattern for i in only_aplh_password ):
        end_list_of_det_pat+=['KEYBOARD_PATTERN']

    list_of_alph= ''.join(i if i in ascii_lowercase else ' ' for i in lower_password ).split()
    list_of_num = ''.join(i if i in digits else ' ' for i in lower_password).split()

    if any( 'abc' in i or 'xyz' in i for i in list_of_alph):
        end_list_of_det_pat+=['ALPHABETICAL_SEQUENCE']

    if any( i in digits or i in digits[::-1] for i in list_of_num):
        end_list_of_det_pat+=['NUMERICAL_SEQUENCE']

    dict_of_symbol_cnt = {lower_password.count(i): i for i in set(lower_password) if lower_password.count(i) > 2}
    if any([lower_password.count(i*3)>=1 for i in dict_of_symbol_cnt.values()]):
        end_list_of_det_pat+=['REPEATED_CHARS']

    if len(password)<8:
        end_list_of_det_pat+=['TOO_SHORT']

    if 8<=len(password)<=12:
        end_list_of_det_pat+=['RECOMMENDED_LONGER']

    if all([not(i in ascii_uppercase)  for i in password]):
        end_list_of_det_pat+=['NO_UPPERCASE']

    if all([not(i in ascii_lowercase) for i in password]):
        end_list_of_det_pat+=['NO_LOWERCASE']

    if all([ not(i in digits)  for i in password]):
        end_list_of_det_pat+=['NO_NUMBERS']

    if all([ not(i in punctuation)  for i in password]):
        end_list_of_det_pat+=['NO_SPECIAL']


    if calculate_entropy(password) < -2.5:
        end_list_of_det_pat+=['LOW_ENTROPY']

    if any(i in password for i in com_eng_word):
        end_list_of_det_pat+=['COMMON_PASSWORD']

    if any(i in password for i in pop_eng_word):
        end_list_of_det_pat+=['COMMON_WORD']

    if any(str(i) in password for i in range(1900, 2025)):
        end_list_of_det_pat+=['YEAR_PATTERN']
    elif any(str(i) in password for i in range(25)):
        end_list_of_det_pat += ['YEAR_PATTERN']
    if len(password)>12:
        end_list_of_det_pat+=['GOOD_LENGTH']

    return end_list_of_det_pat

def calculate_entropy(password: str) -> float:
    entropy = 0
    for i in set(password):
        probability_of_i=password.count(i)/len(password)
        entropy+=(probability_of_i*log(probability_of_i, 2))
    return -entropy if password!='' else 0

def assess_password(password: str) -> Tuple[int, list[str]]:
    end_list=[0, []]
    for i in detect_patterns(password):
        end_list[0]+=PASSWORD_CRITERIA[i]['score']
        end_list[1]+=PASSWORD_CRITERIA[i]['message']
    return end_list

def get_structural_fingerprint(password: str) -> dict:
    """
    Create a structural fingerprint of the password.

    Args:
        password: Input password string

    Returns:
        Dictionary containing:
            - character_types: List of character type by position (upper, lower, digit, special)
            - length: Password length
            - uppercase_positions: List of uppercase letter positions
            - special_positions: List of special character positions
            - number_positions: List of number positions
    """
    pass

def generate_twin(password: str) -> str:
    """
    Generate a new password with the same structural complexity as the input password.

    Args:
        password: Original password to base the twin on

    Returns:
        New password with different characters and same structure
    """
    pass


