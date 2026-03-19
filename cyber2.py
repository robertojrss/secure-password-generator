#cyber2.py

import random
import string

def generate_password(min_length, include_numbers=True, include_special_chars=True):
    # Define groups of characters we can use
    letters = string.ascii_letters            # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = string.digits                   # '0123456789'
    special_characters = string.punctuation   # '!@#$%^&*()_+...'

    # Start with letters, and add more types if requested
    possible_characters = letters
    if include_numbers:
        possible_characters += numbers
    if include_special_chars:
        possible_characters += special_characters

    # Variables to store the password and check its properties
    password = ""
    contains_number = False
    contains_special_char = False
    criteria_met = False

    # Keep adding random characters until length and criteria are satisfied
    while not criteria_met or len(password) < min_length:
        new_character = random.choice(possible_characters)
        password += new_character

        # Update flags if the new character meets a condition
        if new_character in numbers:
            contains_number = True
        if new_character in special_characters:
            contains_special_char = True

        # Check if password meets all user-selected requirements
        criteria_met = True
        if include_numbers:
            criteria_met = contains_number
        if include_special_chars:
            criteria_met = criteria_met and contains_special_char

    return password

# --- Main Program ---
min_length = int(input("Enter the minimum length of the password: "))
want_numbers = input("Should the password include numbers? (y/n): ").lower() == 'y'
want_special_chars = input("Should the password include special characters? (y/n): ").lower() == 'y'

generated_password = generate_password(min_length, want_numbers, want_special_chars)
print("Your generated password is:", generated_password)