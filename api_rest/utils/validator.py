import datetime
import re


def is_valid_blank_field(field):
    """
    Function to validate blank field.
    @param field:
    @return: bool True if is valid, otherwise False
    """
    regex = "^\s*$"
    if re.search(regex, field):
        raise ValueError("")

    return field


def is_valid_email(email):
    """
    Function to validate Email.
    @param email:
    @return: bool True if is valid, otherwise False
    """
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if re.search(regex, email):
        return email

    raise ValueError("")


def is_valid_date(data):
    """
    Function to validate Date.
    @param data:
    @return bool True if is valid, otherwise False
    """
    try:
        datetime.datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_cpf(cpf):
    """
    Function to validate CPF.
    @param cpf:
    @return bool True if is valid, otherwise False
    """
    # Check if type is str
    if not isinstance(cpf, str):
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]", "", cpf)

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    sum = 0
    weight = 10

    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum += int(cpf[n]) * weight

        # Decrement weight
        weight -= 1

    verifyingDigit = 11 - sum % 11

    if verifyingDigit > 9:
        firstVerifyingDigit = 0
    else:
        firstVerifyingDigit = verifyingDigit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum += int(cpf[n]) * weight

        # Decrement weight
        weight -= 1

    verifyingDigit = 11 - sum % 11

    if verifyingDigit > 9:
        secondVerifyingDigit = 0
    else:
        secondVerifyingDigit = verifyingDigit

    if cpf[-2:] == "%s%s" % (firstVerifyingDigit, secondVerifyingDigit):
        return True
    return False
