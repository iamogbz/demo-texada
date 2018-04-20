"""
Api views module
"""

from django.db.models import ProtectedError
from rest_framework import (
    mixins,
    status,
    viewsets,
)
from rest_framework.exceptions import APIException
from rest_framework.decorators import detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import (
    Package,
    Status,
)
from .serializers import (
    PackageSerializer,
    PackageStatusSerializer,
    StatusSerializer,
)


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows packages to be tracked or updated.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    pagination_class = LimitOffsetPagination

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            detail = 'Can not delete package with tracking information'
            exc = APIException(detail)
            exc.status_code = status.HTTP_400_BAD_REQUEST
            response = exception_handler(exc, None)
            return response

    def get_serializer_class(self):
        if self.action == 'tracking':
            serializer_class = PackageStatusSerializer
        else:
            serializer_class = super().get_serializer_class()
        return serializer_class

    @detail_route(methods=['GET', 'POST'], url_path='tracking')
    def tracking(self, request, pk=None):
        """
        Handle showing and updating of tracking information
        """
        if request.method == 'GET':
            statuses = self.paginate_queryset(
                Status.objects.filter(package=pk))
            serializer = PackageStatusSerializer(
                statuses, many=True, context={'request': request})
            response = self.get_paginated_response(serializer.data)
        elif request.method == 'POST':
            data = request.data.copy()
            data['package'] = PackageSerializer(
                self.get_object(), context={'request': request}).data['url']
            serializer = StatusSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response


class StatusViewSet(mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint that allows status to be viewed or modified.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
