"""
Management command to check and diagnose email configuration status.
Shows if email is properly set up and sends a test email.
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check email configuration status and test email sending'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            type=str,
            help='Send a test email to the specified address'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed configuration info'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📧 Email Configuration Checker\n'))
        self.print_config_status()

        if options['verbose']:
            self.print_detailed_config()

        if options['test']:
            self.send_test_email(options['test'])

    def print_config_status(self):
        """Print basic email configuration status"""
        email_host = getattr(settings, 'EMAIL_HOST', 'NOT SET')
        email_port = getattr(settings, 'EMAIL_PORT', 'NOT SET')
        email_use_tls = getattr(settings, 'EMAIL_USE_TLS', False)
        email_use_ssl = getattr(settings, 'EMAIL_USE_SSL', False)
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
        email_host_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')

        self.stdout.write('\n🔧 Email Configuration:')
        self.stdout.write(f'  Email Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'  SMTP Host: {email_host}')
        self.stdout.write(f'  SMTP Port: {email_port}')
        self.stdout.write(f'  Use TLS: {email_use_tls}')
        self.stdout.write(f'  Use SSL: {email_use_ssl}')
        self.stdout.write(f'  Timeout: {settings.EMAIL_TIMEOUT}s')

        # Check if email is configured
        if not email_host_user or not email_host_password:
            self.stdout.write(self.style.WARNING('\n⚠️  Email NOT Fully Configured'))
            self.stdout.write('  Missing: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD')
            self.stdout.write('  Result: Emails will NOT be sent')
            self.stdout.write('\n  To fix, set these environment variables:')
            self.stdout.write('    EMAIL_HOST_USER=your-email@gmail.com')
            self.stdout.write('    EMAIL_HOST_PASSWORD=your-app-password')
            return False
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Email Configured'))
            self.stdout.write(f'  Host User: {email_host_user}')
            self.stdout.write(f'  Password: {"*" * len(email_host_password)}')
            self.stdout.write(f'  From Email: {from_email}')
            return True

    def print_detailed_config(self):
        """Print detailed configuration information"""
        self.stdout.write('\n📋 Detailed Configuration:')
        self.stdout.write(f'  DEBUG: {settings.DEBUG}')
        self.stdout.write(f'  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')

        email_settings = {
            'EMAIL_BACKEND': settings.EMAIL_BACKEND,
            'EMAIL_HOST': settings.EMAIL_HOST,
            'EMAIL_PORT': settings.EMAIL_PORT,
            'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
            'EMAIL_USE_SSL': settings.EMAIL_USE_SSL,
            'EMAIL_HOST_USER': '***' if settings.EMAIL_HOST_USER else 'NOT SET',
            'EMAIL_HOST_PASSWORD': '***' if settings.EMAIL_HOST_PASSWORD else 'NOT SET',
            'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
            'EMAIL_TIMEOUT': settings.EMAIL_TIMEOUT,
        }

        for key, value in email_settings.items():
            self.stdout.write(f'  {key}: {value}')

    def send_test_email(self, recipient_email):
        """Send a test email to verify configuration"""
        self.stdout.write(f'\n📤 Sending test email to {recipient_email}...')

        try:
            subject = 'PaperAIzer - Test Email'
            message = f"""Hello,

This is a test email from PaperAIzer to verify email configuration is working correctly.

If you received this, your email setup is functioning properly! ✅

Sent at: {__import__('datetime').datetime.now()}

Best regards,
PaperAIzer Team"""

            from_email = settings.DEFAULT_FROM_EMAIL
            result = send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

            if result == 1:
                self.stdout.write(self.style.SUCCESS(f'\n✅ Test email sent successfully!'))
                self.stdout.write(f'  To: {recipient_email}')
                self.stdout.write(f'  From: {from_email}')
                self.stdout.write(f'  Subject: {subject}')
            else:
                self.stdout.write(self.style.WARNING(f'\n⚠️  Email sent but no confirmation'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Failed to send test email'))
            self.stdout.write(f'  Error: {str(e)}')
            self.stdout.write(f'  Type: {type(e).__name__}')
            self.stdout.write('\n  Common causes:')
            self.stdout.write('  1. Wrong EMAIL_HOST_USER or EMAIL_HOST_PASSWORD')
            self.stdout.write('  2. SMTP server connection failed')
            self.stdout.write('  3. Firewall blocking SMTP port')
            self.stdout.write('  4. Gmail account security settings')
            logger.error(f'Email test failed: {str(e)}', exc_info=True)
