from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from library.permissions import IsLibrarian
from library.serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowRecordSerializer
from library.models import Author, Book, Member, BorrowRecord
from library.paginations import SimplePagination
from drf_yasg.utils import swagger_auto_schema


class AuthorViewSet(viewsets.ModelViewSet):
    """Author API: CRUD operations for authors."""
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'name']
    pagination_class = SimplePagination
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List authors",
        operation_description="Retrieve all authors"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve author",
        operation_description="Retrieve details of a specific author by ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class BookViewSet(viewsets.ModelViewSet):
    """Book API: CRUD operations for books."""
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['title', 'isbn', 'category', 'author__name']
    pagination_class = SimplePagination
    permission_classes = [IsAuthenticated, IsLibrarian]

    @swagger_auto_schema(
        operation_summary="List books",
        operation_description="Retrieve all books"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve book",
        operation_description="Retrieve details of a specific book by ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class MemberViewSet(viewsets.ModelViewSet):
    """Member API: CRUD operations for members."""
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['id', 'email']
    pagination_class = SimplePagination
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List members",
        operation_description="Retrieve all members"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve member",
        operation_description="Retrieve details of a specific member by ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    """BorrowRecord API: Manage borrowing and returning of books."""
    serializer_class = BorrowRecordSerializer
    queryset = BorrowRecord.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['book__title', 'member__email']
    pagination_class = SimplePagination
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='post',
        request_body=BorrowRecordSerializer,
        responses={201: BorrowRecordSerializer},
        operation_description="Borrow a book for a member"
    )
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

    @swagger_auto_schema(
        method='post',
        responses={200: BorrowRecordSerializer},
        operation_description="Return a borrowed book"
    )
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()

        if borrow_record.return_date:
            return Response({"error": "Book already returned"}, status=status.HTTP_400_BAD_REQUEST)
        if borrow_record.book.availability_status:
            return Response({"error": "This book is already available in the library. Invalid return."}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.book.availability_status = True
        borrow_record.book.save()
        borrow_record.return_date = now().date()
        borrow_record.save()

        return Response(self.get_serializer(borrow_record).data, status=status.HTTP_200_OK)
