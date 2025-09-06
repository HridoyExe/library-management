from rest_framework.pagination import PageNumberPagination

class SimplePagination(PageNumberPagination):
    page_size = 5