def is_tue_email(email: str) -> bool:
    return email.endswith("@student.tue.nl") or email.endswith("@alumni.tue.nl")


def is_fontys_email(email: str) -> bool:
    return email.endswith("@fontys.nl")


def is_valid_institutional_email(email: str) -> bool:
    return is_tue_email(email) or is_fontys_email(email)
