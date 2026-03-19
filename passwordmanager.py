import secrets
import string
import math
import random

# Common passwords (based on public breach reports)
COMMON_PASSWORDS = {
    "123456", "12345678", "123456789", "12345", "password", "admin", "qwerty",
    "abc123", "111111", "123123", "1234567890", "1234567", "letmein", "welcome",
    "monkey", "sunshine", "princess", "iloveyou", "admin123", "pass@123", "Aa123456",
    "password1", "1234", "000000", "qwerty123", "P@ssw0rd"
}


def build_charset(use_lower, use_upper, use_digits, use_special):
    chars = ""
    if use_lower:
        chars += string.ascii_lowercase
    if use_upper:
        chars += string.ascii_uppercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += string.punctuation
    return chars


def generate_password(length, use_lower=True, use_upper=True, use_digits=True, use_special=True):
    if length < 4:
        raise ValueError("Minimum length is 4")

    charset = build_charset(use_lower, use_upper, use_digits, use_special)

    if not charset:
        raise ValueError("Select at least one character type")

    # Ensure at least one character from each selected type
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_special:
        pools.append(string.punctuation)

    if length < len(pools):
        raise ValueError(f"Minimum length must be {len(pools)} to include all selected types")

    password = [secrets.choice(pool) for pool in pools]

    while len(password) < length:
        password.append(secrets.choice(charset))

    secrets.SystemRandom().shuffle(password)

    return "".join(password), len(charset)


def calculate_entropy(length, charset_size):
    return length * math.log2(charset_size) if charset_size > 1 and length > 0 else 0.0


def estimate_crack_time(entropy_bits):
    if entropy_bits < 40:
        return "instant / seconds"
    if entropy_bits < 55:
        return "minutes to hours"
    if entropy_bits < 65:
        return "days to weeks"
    if entropy_bits < 80:
        return "months to years"
    if entropy_bits < 100:
        return "thousands to millions of years"
    if entropy_bits < 120:
        return "billions of years"
    return "practically impossible (trillions+ of years)"


def check_patterns(password):
    issues = []

    if password.lower() in COMMON_PASSWORDS:
        issues.append("very common password")

    if password.isdigit() or password.isalpha():
        issues.append("single character class")

    return issues


def evaluate_strength(password, charset_size):
    entropy = calculate_entropy(len(password), charset_size)
    issues = check_patterns(password)

    if "very common password" in issues:
        strength = "Very Weak"
        adjusted_entropy = 10.0
    else:
        adjusted_entropy = entropy
        if entropy >= 100:
            strength = "Very Strong"
        elif entropy >= 80:
            strength = "Strong"
        elif entropy >= 60:
            strength = "Good"
        else:
            strength = "Weak"

    return strength, entropy, adjusted_entropy, issues


def get_valid_length():
    """Get and validate password length"""
    while True:
        try:
            length = input("Password length: ").strip()
            if not length:
                print("Please enter a number.")
                continue
            length = int(length)
            if length < 4:
                print("Minimum length is 4. Please try again.")
                continue
            return length
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_yes_no_input(prompt):
    """Get and validate y/n input"""
    while True:
        answer = input(prompt + " (y/n): ").lower().strip()
        if answer in ['y', 'n', '']:
            return answer != 'n'  # Enter or 'y' = True, 'n' = False
        print("Please type 'y' or 'n'.")


def main():
    print("# Secure Password Generator #\n")

    # Get password length with validation
    length = get_valid_length()
    
    print("\nSelect character types:")
    use_lower = get_yes_no_input("Lowercase?")
    use_upper = get_yes_no_input("Uppercase?")
    use_digits = get_yes_no_input("Numbers?")
    use_special = get_yes_no_input("Special characters?")

    try:
        pwd, char_count = generate_password(
            length, use_lower, use_upper, use_digits, use_special
        )
    except ValueError as e:
        print(f"Error: {e}")
        return

    strength, entropy, adj_entropy, issues = evaluate_strength(pwd, char_count)
    crack_time = estimate_crack_time(entropy)

    print("\n" + "=" * 50)
    print(f"Generated password: {pwd}")
    print(f"Strength:           {strength}")
    print(f"Entropy:            {entropy:.1f} bits")
    print(f"Estimated crack time: {crack_time}")

    if issues:
        print(f"Warnings:           {', '.join(issues)}")

    if entropy < 60:
        print("Recommendation: use at least 12-16 characters with mixed types")

    print("=" * 50)


if __name__ == "__main__":
    main()