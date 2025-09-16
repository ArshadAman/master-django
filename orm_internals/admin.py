# orm_internals/admin.py
from django.contrib import admin
from .models import Article, Author

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # --- Optimizations ---      
    # 1. Use list_display to show the author's name directly
    list_display = ('title', 'author_name', 'views')

    # 2. Use list_select_relateed to pre-fetch the author data in a single JOIN
    # This is the key fisx for the N+1 problem in the admin.

    list_select_related = ('author', )

    # 3. Add pagination to limit the number of items per page
    list_per_page = 25

    # 4. Add Search functionality
    search_fields = ('title', 'author__name')

    # 5. Add filters
    list_filter = ('author', )

    # A custom method to dispay the author's name
    def author_name(self, obj):
        return obj.author.name
    
    # Set a user-friendly column header for the custom method
    author_name.short_description = 'Author'

# Also register the author model so we can manage authors
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name', )