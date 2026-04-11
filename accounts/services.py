from password_validator import PasswordValidator

def validae_password(password):
    schema = PasswordValidator()

    # Add properties to it
    schema\
    .min(8)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()\

    # Validate against a password string
    is_valid= schema.validate(password)
