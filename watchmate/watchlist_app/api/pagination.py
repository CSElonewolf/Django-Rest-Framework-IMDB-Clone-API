from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination


class WatchListPagination(PageNumberPagination):
	page_size = 5
	page_query_param = 'pg'
	page_size_query_param ='size'
	max_page_size = 7
	last_page_strings  = 'end'

class WatchListLOPagination(LimitOffsetPagination):
	default_limit = 5
	max_limit = 12
	limit_query_param ='limit'
	# offset_query_param  = 'start'


class WatchListCPagination(CursorPagination):
	page_size = 5
	ordering  = 'created'