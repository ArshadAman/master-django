# orm_internals/management/commands/populate_articles.py
from django.core.management.base import BaseCommand
from orm_internals.models import Author, Article
import random

class Command(BaseCommand):
    help = 'Populates the database with a large number of articles.'

    def handle(self, *args, **options):
        if Article.objects.count() > 500:
            print("Database already populated.")
            return

        print("Populating database...")
        authors = [Author.objects.create(name=f"Author {i}") for i in range(20)]
        for i in range(1000):
            Article.objects.create(
                author=random.choice(authors),
                title=f"Article Title Number {i}",
                views=random.randint(0, 5000)
            )
        print("Population complete.")