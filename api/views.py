from django.http import JsonResponse
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.exceptions import APIException
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import Package, Status
from .serializers import *


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows packages to be viewed or edited.
    """
    queryset = Package.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as exception:
            detail = 'Can not delete package with tracking information'
            exc = APIException(detail)
            exc.status_code = status.HTTP_400_BAD_REQUEST
            response = exception_handler(exc, None)
            return response

    def get_serializer_class(self):
        if self.action == 'get_tracking':
            return PackageStatusSerializer
        return PackageSerializer

    @detail_route(methods=['GET', 'POST'], url_path='tracking')
    def get_tracking(self, request, pk, format=None):
        if (request.method == 'GET'):
            statuses = Status.objects.filter(package=pk)
            serializer = PackageStatusSerializer(
                statuses, many=True, context={'request': request})
            return Response(serializer.data)
        elif (request.method == 'POST'):
            data = request.data.copy()
            data['package'] = PackageSerializer(
                self.get_object(), context={'request': request}).data['url']
            serializer = StatusSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint that allows status to be created and viewed.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
