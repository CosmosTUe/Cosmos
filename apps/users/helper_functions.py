def is_tue_email(email: str) -> bool:
    return email.endswith("@tue.nl")


def is_fontys_email(email: str) -> bool:
    return email.endswith("@fontys.nl")


def is_valid_institutional_email(email: str) -> bool:
    # Temporarily remove fontys support
    # return is_tue_email(email) or is_fontys_email(email)
    return is_tue_email(email)


def same_email_institution(*emails) -> bool:
    tue = sum(map(lambda x: is_tue_email(x), emails))
    fontys = sum(map(lambda x: is_fontys_email(x), emails))
    return (tue == 0) or (fontys == 0)
