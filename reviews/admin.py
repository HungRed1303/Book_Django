from django.contrib import admin
from reviews.models import (Publisher, Contributor, Book,
BookContributor, Review)

class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn')
    list_filter = ('publisher', 'publication_date')
    search_fields = ('title', 'isbn')

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('creator', 'book')}),
        ('Review content', {'fields': ('content', 'rating')})
    )

class ContributorAdmin(admin.ModelAdmin):
    search_fields = ('first_names', 'last_names__startswith')
    list_display = ('first_names', 'last_names')
    list_filter = ('last_names',)

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Contributor,ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)
