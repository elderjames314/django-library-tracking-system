from unittest.mock import patch
from django.test import TestCase
from library.models import Author, Loan, Book, Member
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from library.tasks import send_daily_loan_overdue_notification




class TestLoanOverdueNotification(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="James", last_name="Oladimeji")
        
        self.book = Book.objects.create(
           title="Poor dad Rich dad",
           isbn="423333",
           genre="fiction",
           available_copies=50
        )

        self.user = User.objects.create_user(username="ojames314", email="ojames314@gmail.com")
        self.member = Member.objects.create(user=self.user)

    @patch("library.send_mail")
    def test_send_daily_loan_notification_send_email_when_loan_is_overdue(self, mock_send_email):
        #PREPARE
        today = timezone.now().date()
        Loan.objects.create(
            book=self.book,
            author = self.author,
            due_date = today + timedelta(days=1) # this shows the loan has been overdue for one day
        )

        #ACT
        send_daily_loan_overdue_notification()

        #ASSERT
        self.assertEqual(mock_send_email.call_count, 1) # test at least the  send email is called once.


    @patch("library.send_mail")
    def test_send_daily_loan_notification_not_send_email_when_loan_is_not_overdue(self, mock_send_email):
        #PREPARE
        Loan.objects.delete() # delete all loans
        
        today = timezone.now().date()
        Loan.objects.create(
            book=self.book,
            author = self.author,
            due_date = today - timedelta(days=1) # This is means, this loand will be overdue in two days time
        )

        #ACT
        send_daily_loan_overdue_notification()

        #ASSERT
        self.assertEqual(mock_send_email.call_count, 1) # test at least the  send email is called once.



