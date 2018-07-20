import logging
import traceback
from logging import CRITICAL, ERROR
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.shortcuts import \
    get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import (
    BadHeaderError, send_mail)
from django.template.loader import \
    render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import \
    urlsafe_base64_encode

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
    mail_validation_error = ''

    #this is getter
    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    #this is setter
    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError('Cannot set mail_sent attribute')

    def log_mail_error(self, **kwargs):
        msg_list = [
            'Activation email didn\'t send.\n',
            'from_email: {from_email}\n'
            'subject: {subject}\n'
            'message: {message}\n',
        ]
        recipient_list = kwargs.get('recipient_list', [])
        for recipient in recipient_list:
            msg_list.insert(
                1, 'recipient: {r}\n'.format(r=recipient)
            )
        if 'error' in kwargs:
            level = ERROR
            error_msg = (
                'error: {0.__class__.__name__}\n'
                'args: {0.args}\n'
            )
            error_info = error_msg.format(
                kwargs['error']
            )
            msg_list.insert(1, error_info)
        else:
            level = CRITICAL
        msg = ''.join(msg_list).format(**kwargs)
        logger.log(level, msg)

    #message is rendered here using render to string
    def get_message(self, **kwargs):
        email_template_name = kwargs.get(
            'email_template_name'
        )
        context = kwargs.get('context')
        print('\n\ngoing to render email_text\n\n')
        email = render_to_string(email_template_name, context)
        print('\n\nemail render successful\n\n')
        return email

    # ensure that the subject is a single line long to avoid the BadHeader exception.
    #BadHeaderException
    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get(
            'subject_template_name'
        )
        context = kwargs.get('context')
        subject = render_to_string(subject_template_name, context)
        #This split the lines and join them together to form single line sentence
        subject = ''.join(subject.splitlines())
        return subject

    #this builds context required for above subject and messages
    def get_context_data(self, request, user, context=None):
        print('I am in get_context_date\n\n\n')
        if context is None:
            context = dict()
            current_site = get_current_site(request)
            #is_secure returns True if protocol is HTTPS
            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
            print("token: {token}\nuid: {uid}".format(token=token, uid=uid))
            context.update({
                'domain': current_site.domain,
                'protocol': protocol,
                'site_name': current_site.name,
                'token': token,
                'uid': uid,
                'user': user,
            })
            print(context)
            return context

    def _send_mail(self, request, user, **kwargs):
        """
        This returns tuple (_mail_sent, err_code)
        """
        kwargs['context'] = self.get_context_data(
            request, user
        )
        mail_kwargs = {
            'subject': self.get_subject(**kwargs),
            'message': self.get_message(**kwargs),
            'from_email': (
                settings.DEFAULT_FROM_EMAIL),
            'recipient_list': [user.email, ]
        }
        try:
            number_sent = send_mail(**mail_kwargs)
        except Exception as error:
            #we don't want to let the user know error has occured
            #instead we log the error
            self.log_mail_error(
                error=error, **mail_kwargs
            )
            if isinstance(error, BadHeaderError):
                err_code = 'badheader'
            elif isinstance(err_code, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpected_error'
            return (False, err_code)
        else:
            if number_sent > 0:
                return (True, None)
            #in case exceptions didn't get caught
            #just a safety precaution
            self.log_mail_error(**mail_kwargs)
            return (False, 'unknownerror')

    def send_mail(self, user, **kwargs):
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = ['  ' + line for line in tb]
            #logging that send_mail called without request
            #at warning level
            logger.warning(
                'send_mail called without '
                'request.\nTraceback:\n{}'.format(
                    ''.join(tb)
                )
            )
            self._mail_sent = False
            return self.mail_sent
        self._mail_sent, error = (
            self._send_mail(request, user, **kwargs)
        )
        if not self.mail_sent:
            self.add_error(
                None,
                ValidationError(self.mail_validation_error,
                                code=error)
            )
        return self.mail_sent


# ActivationMailFormMixin expects some contexts
class MailContextViewMixin:
    email_template_name = 'accounts/email_create.txt'
    subject_template_name = 'accounts/subject_create.txt'

    def get_save_kwargs(self, request):
        return {
            'email_template_name': self.email_template_name,
            'request': request,
            'subject_template_name': self.subject_template_name,
        }


