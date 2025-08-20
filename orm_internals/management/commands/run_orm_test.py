from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from orm_internals.models import Article

def run_experiments():
    # populate db if empty
    if not Article.objects.exists():
        print("Populating the database")
        Article.objects.create(title = "Article 1")
        Article.objects.create(title = "Article 1")
    
    print("\n--- Experiment: Creating a QuerySet is Lazy ---")
    reset_queries()
    # This line doesnot hit the database
    articles_qs = Article.objects.all()
    print(f"Number of queries after creating queryset: {len(connection.queries)}")

    print("\n--- Experiment: Iteration triggers evaluation ---")
    reset_queries()
    for article in articles_qs:
        # The articles_qs is now warm with a cache
        # This second loop uses the cache and does NOT hit the database
        print("Iterating a second time...") 
        for article in articles_qs:
            pass
        print(f"Number of queries on second iteration: {len(connection.queries)}")

        print("\n--- Experiment: Refining a queryset clones it ---")
        reset_queries()
        # This filter() clones the original queryset but doesnot HIT the databse
        filtered_qs = Article.objects.filter(title__contains = '1')
        print(f"Number of queries after filtering: {len(connection.queries)}")

        print("Evaluating the new, filterd queryset")
        # Thisw evaluation hits the database with a new WHERE clause.
        list(filtered_qs)
        print(f"Number of queries after evaluating clone: {len(connection.queries)}")
class Command(BaseCommand):
    help = "Runs ORM laziness experiements"

    def handle(self, *args, **options):
        run_experiments()