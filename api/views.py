from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

from .models import Package, Status
from .serializers import PackageSerializer, StatusSerializer


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows packages to be viewed or edited.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as exception:
            detail = 'Can not delete package with tracking information'
            print(detail)
            exc = APIException(detail)
            exc.status_code = status.HTTP_400_BAD_REQUEST
            response = exception_handler(exc, None)
            return response



class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows status to be created and viewed.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
