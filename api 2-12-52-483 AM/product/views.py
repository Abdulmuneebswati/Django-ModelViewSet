from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination  # Apply pagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)  # Enable filtering and searching
    ordering_fields = ['name', 'price', 'created_at']
    search_fields = ['name', 'description']

    def create(self, request, *args, **kwargs):

        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            if isinstance(request.data, list):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.data[0], status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e), "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

