from rest_framework import serializers
from .models import Package
from .models import Status


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'description',)


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ('package', 'latitude', 'longitude', 'elevation',)
