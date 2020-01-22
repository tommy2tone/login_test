import re

def valid_password(password):
    
    if len(password) < 8:
        # print('password not long enough')
        message = 'Password must be atleast 8 characters.'
        return message
    elif len(password) > 32:
        message = 'Password cannot be more than 32 characters'
        return message
    elif not re.search('[a-z]', password):
        message = 'Password must contain atleast 1 lower case letter.'
        return message
    elif not re.search('[A-Z]', password):
        message = 'Password must contain atleast 1 upper case letter.'
        return message
    elif not re.search('[0-9]', password):
        message = 'Password must contain atleast 1 number'
        return message
    elif re.search(r'[\s]', password):
        message = 'Password cannot contain spaces.'
        return message
    elif not re.search('[!@#$%^&*]', password):
        message = 'Password must contain at least 1 special character.'
        return message
    else:
        return True