from rest_framework import viewsets, pagination
from rest_framework_gis.filters import InBBOXFilter

from .models import Municipality
from .serializers import MunicipalitySerializer
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


class MunicipalityPagination(pagination.PageNumberPagination):
    page_size = 100

class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalitySerializer
    pagination_class = GeoJsonPagination
    bbox_filter_field = 'geom'
    filter_backends = (InBBOXFilter,)
    # bbox_filter_include_overlapping = True
    authentication_classes = (JWTAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
