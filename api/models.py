from django.db import models


class Package(models.Model):
    """
    Model defining a package
    .id - Unique identifier for package, auto generated on insert.
    .description - Description of package.
    """

    description = models.CharField(max_length=140, blank=False)

    def __str__(self):
        return self.description

    def __unicode__(self):
        return str(self).encode()

    class Meta:
        ordering = ('id',)


class Status(models.Model):
    """
    Status of a package
    .created = Server time of the status update
    .package = Foreign key relationship to package (package_id)
    .latitude = Latitude of package to 8 decimal places
    .longitude = Longitude of package to 8 decimal places
    .elevation = Vertical elevation of package in metres to 3 decimal places (millimetre)
    """

    created = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(editable=False)
    package = models.ForeignKey(
        Package, on_delete=models.PROTECT, related_name="tracking")
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    elevation = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return "{0} at lat({1}) lng({2}), {3} metres high".format(
            self.created, self.latitude, self.longitude, self.elevation)

    def __unicode__(self):
        return str(self).encode()

    class Meta:
        ordering = ('package', 'created',)
