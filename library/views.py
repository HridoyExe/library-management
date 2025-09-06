from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from library.serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowRecordSerializer
from library.models import Author, Book, Member, BorrowRecord
from rest_framework.filters import SearchFilter
from library.paginations import SimplePagination
from django.utils.timezone import now


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']
    pagination_class = SimplePagination


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'isbn', 'category', 'author__name']
    pagination_class = SimplePagination


class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'email']
    pagination_class = SimplePagination


class BorrowRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowRecordSerializer
    queryset = BorrowRecord.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['book__title', 'member__email']
    pagination_class = SimplePagination

    @action(detail=False, methods=['post'])
    def borrow_book(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']
        member = serializer.validated_data['member']

        if not book.availability_status:
            return Response({"error": "This Book is not available"}, status=status.HTTP_400_BAD_REQUEST)
        if BorrowRecord.objects.filter(book=book, member=member, return_date__isnull=True).exists():
            return Response({"error": "This member already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)
        book.availability_status = False
        book.save()
        borrow_record = BorrowRecord.objects.create(book=book, member=member)

        return Response(self.get_serializer(borrow_record).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()

        if borrow_record.return_date:
            return Response({"error": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST)
        borrow_record.book.availability_status = True
        borrow_record.book.save()
        borrow_record.return_date = now().date()
        borrow_record.save()

        return Response(self.get_serializer(borrow_record).data, status=status.HTTP_200_OK)
