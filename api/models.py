"""
Define api models
"""

from django.db import models
from django.utils import timezone


class Package(models.Model):
    """
    Model defining a package
    .id - Unique identifier for package, auto generated on insert.
    .description - Description of package.
    """

    description = models.CharField(max_length=140, blank=False)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ('id',)


class Status(models.Model):
    """
    Status of a package
    .created = Server time of the status update
    .package = Foreign key relationship to package (package_id)
    .latitude = Latitude of package to 6 decimal places
    .longitude = Longitude of package to 6 decimal places
    .elevation = Vertical elevation of package in metres to 3 decimal places (millimetre)
    """

    created = models.DateTimeField(editable=False, default=timezone.now)
    package = models.ForeignKey(
        Package, on_delete=models.PROTECT, related_name="tracking")
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return "{0} at lat({1}) lng({2}), {3} metres high".format(
            self.created, self.latitude, self.longitude, self.elevation)

    class Meta:
        ordering = ('-created',)
