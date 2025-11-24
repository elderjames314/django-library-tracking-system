from django.test import TestCase
from library.models import Author, Book, Loan, Member
from django.contrib.auth.models import User


class TestLoandExtension(TestCase):
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
    