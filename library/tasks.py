from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.template.context_processors import request
from datetime import timedelta
from library.models import Loan
import logging


logger = logging.getLogger(__name__)

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass
# task to send daily loan overdue.
# we set bind True to automatically retry incase if email faile
# also we set max retry to be 5 time before sending to dead letter queue
@shared_task(bind=True, max_retries=5, default_later_retry=60)
def send_daily_loan_overdue_notification(self):
    try:

        today = timezone.now().date()
        overdue_loans = Loan.objects.filter(
            due_date__lt=today,
            is_returned=False,
            has_daily_overdue_loan_notification_sent=False
        )
        # check if no overdule loands
        if overdue_loans.count() == 0:
            logging.info("No overdue loans found")
            return
        
        for loan in overdue_loans:
            send_mail(
                subject='Daily Loan Overdue Notification',
                message=f'Dear {loan.member.user.username}, this is to inform you that book you loaned was overdue today. Kindly return it on time to avoid fine.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False,
            )
        logging.info(f"The total overdue loans found:: {overdue_loans.count()}")
        return "Task completed"
    except Exception as exec:
        if self.max_retries > request.retries:
            # SEND IT TO DEAD LETTER QUEUE.
            logger.info("Max retries exceeded")
            raise("Email could not be send after pass retry")



