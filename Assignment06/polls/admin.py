from polls.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PA(admin.ModelAdmin):
    fieldsets = [
            (None,          {'fields': ['question']}),
            ('Date Info',   {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    # Modifies the headers of the table for the various pages in the admin page
    list_display = ('question', 'pub_date', 'was_published_today')

    # adds the sidebar for filter options based on the type of the field - this case datetime
    list_filter = ['pub_date']

    # adds a search box and searches the field specified
    search_fields = ['question']

    # adds a hierarchical nav by date at top of change list page
    date_hierarchy = 'pub_date'

admin.site.register(Poll, PA)