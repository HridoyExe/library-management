from django.contrib import admin
from .models import Author, Book, Member, BorrowRecord

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'biography')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'category', 'availability_status')
    list_filter = ('availability_status', 'category')
    search_fields = ('title', 'isbn')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'membership_date')
    search_fields = ('name', 'email')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'member', 'borrow_date', 'return_date')
    list_filter = ('borrow_date', 'return_date')
