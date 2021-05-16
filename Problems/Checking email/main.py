def check_email(string):
    if " " in string.strip():
        return False
    elif "@" not in string or "." not in string:
        return False
    elif "@." in string:
        return False
    # Check if the "." comes after "@" by comparing indices in the reversed string
    if string[::-1].index(".") > string[::-1].index("@"):
        return False
    else:
        return True
