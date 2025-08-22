from django.core.management.base import BaseCommand
from django.db.models import Count, Avg, Subquery, OuterRef
from orm_internals.models import Article, Author

def setup_data():
    """Create some sample data."""
    if Author.objects.exists():
        return # Dont recreate data
    print("Settings up sample data....")
    author1 = Author.objects.create(name="Alice")
    author2 = Author.objects.create(name="Bob")
    Article.objects.create(author=author1, title="Alice's First Article", views=150)
    Article.objects.create(author=author1, title="Alice's Second Article", views=250)
    Article.objects.create(author=author2, title="Bob's Great Article", views=500)

def run_complex_query():
    """Build a complex query and inspect its SQL."""
    setup_data() # Create sample data if not exits

    # Goal: Get each author and annotate with their article count
    # and the title of their most viewd article

    # 1. Create a subquery to find the title of the most viewed article for an author

    most_viewed_subquery = Subquery(
        Article.objects.filter(
            author = OuterRef('pk')
        ).order_by('-views').values('title')[:1]
    )

    # 2. Build the main queryset with annotations
    author_qs = Author.objects.annotate(
        article_count = Count('article'),
        most_viwed_article_title = most_viewed_subquery
    )

    # 3. Get the SQLCompiler and generate the SQL
    # This is how you can inspect the query without executing it
    sql, params = author_qs.query.sql_with_params()
    print("\n--- Generated SQL ---")
    print(sql)
    print("\n--- Parameters ---")
    print(params)

    # 4. Run Explain on the query in your DB shell
    print("\n--- To run EXPLAIN in your database shell: ---")
    # Replace placeholders with actual param values for explain
    explain_sql = sql % tuple(f"'{p}'" for p in params)
    print(f"Explain {explain_sql};")

    print("\n--- Actual Query Results ---")
    for author in author_qs:
        print(f"{author.name} (Articles: {author.article_count}) - Top Article: {author.most_viwed_article_title}")

class Command(BaseCommand):
    help = 'Demonstrates the SQL Compiler'

    def handle(self, *args, **options):
        run_complex_query()