from django.core.validators import RegexValidator, ValidationError




def email_validator(value):
    email_domain = value.split('@')[1]
    if not email_domain == 'bmsce.ac.in':
        raise ValidationError(
            message = 'Please enter email provided by your college. {email_domain}',
            code='email_err',
            params={'email_domain': email_domain}
        )