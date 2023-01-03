from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class MyPagination(PageNumberPagination):
    page_size = 10       # 默认每页显示多少条
    page_query_param = 'page_num'     # 指定查询第几页（页码），默认 page
    page_size_query_param = 'page_size'   # 定义每页显示多少条
    max_page_size = 100     # 每页最多显示多少条

    def get_paginated_response(self, data):
        code = 200
        msg = "成功"
        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('data', data)
        ]))