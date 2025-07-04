from rest_framework import viewsets
from django.utils.dateparse import parse_datetime
from .models import LogData
from .serializers import LogDataSerializer


class LogDataViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogDataSerializer

    def get_queryset(self):
        queryset = LogData.objects.all()
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if start and end:
            queryset = queryset.filter(date_logged__gte=parse_datetime(start),
                                       date_logged__lte=parse_datetime(end))
        return queryset
