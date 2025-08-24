from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from orm_internals.models import Author, Article, Tag
import time

def setup_data():
    # Clear existing data to ensure a clean run
    Article.objects.all().delete()
    Author.objects.all().delete()
    Tag.objects.all().delete()

    print("Setting up sample data...")
    tag1 = Tag.objects.create(name="Tech")
    tag2 = Tag.objects.create(name="News")
    author1 = Author.objects.create(name="Alice")
    author2 = Author.objects.create(name="Bob")

    # Create the articles and then add tags to them
    alice_art1 = Article.objects.create(author=author1, title="Alice's First Article", views=100)
    alice_art1.tags.add(tag1, tag2)

    alice_art2 = Article.objects.create(author=author1, title="Alice's Second Article", views=200)
    alice_art2.tags.add(tag1)

    bob_art = Article.objects.create(author=author2, title="Bob's Great Article", views=300)
    bob_art.tags.add(tag2)
    print("Sample data created.")


def measure_query_time(func, *args, **kwargs):
    """Utility to measure time and query count of a function"""
    reset_queries()
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    query_count = len(connection.queries)
    duration = (end_time - start_time) * 1000
    print(f"Executed in {duration:.2f}ms with {query_count} queries")

def bad_query():
    """Demonstrate the N+1 Problem"""
    print("\n --- Running BAD query (N+1 Problem)")
    articles = Article.objects.all()
    for article in articles:
        # Accessing article.author triggers a new query for each article
        author_name = article.author.name
        # Accessing article.tags().all() triggers another new query for each article
        tag_name = ", ".join(list(tag.name for tag in article.tags.all()))


def good_query():
    """Fixing the N+1 problem with select_related and prefetched_related"""
    print("\n--- Running GOOD query (optimized) ---")
    articles = Article.objects.select_related('author').prefetch_related('tags')
    for article in articles:
        author_name = article.author.name
        tag_names = ", ".join(tag.name for tag in article.tags.all())
    
class Command(BaseCommand):
    help = "Demonstrate and fixes the N+1 query problem"

    def handle(self, *args, **kwargs):
        setup_data()
        measure_query_time(bad_query)
        measure_query_time(good_query)
