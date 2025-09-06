from django.urls import path, include
from rest_framework_nested import routers
from library.views import AuthorViewSet, BookViewSet, MemberViewSet, BorrowRecordViewSet

# Default router
router = routers.DefaultRouter()
router.register('authors', AuthorViewSet, basename='author')
router.register('books', BookViewSet, basename='book')
router.register('members', MemberViewSet, basename='member')
router.register('borrow-records', BorrowRecordViewSet, basename='borrowrecord')

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('borrow-records', BorrowRecordViewSet, basename='book-borrow-records')

members_router = routers.NestedDefaultRouter(router, 'members', lookup='member')
members_router.register('borrow-records', BorrowRecordViewSet, basename='member-borrow-records')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('', include(members_router.urls)),
]
