from rest_framework.pagination import PageNumberPagination

class CustomNumberPagination(PageNumberPagination):
    page_size= 1
    max_page_size= 5
    page_query_param= 'page'
    #specifies how many pages from the client
    page_size_query_param= 'count'