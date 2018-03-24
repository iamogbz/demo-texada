from .models import Package, Status
from rest_framework import viewsets
from .serializers import PackageSerializer, StatusSerializer


class PackageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows packages to be viewed or edited.
    """
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class StatusViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows status to be created and viewed.
    """
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
