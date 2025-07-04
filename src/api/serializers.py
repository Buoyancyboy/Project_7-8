from rest_framework import serializers
from .models import LogData

class LogDataSerializer(serializers.Serializer):
    topicID = serializers.IntegerField(source='topic_config_ID')
    data = serializers.CharField(source='message')
    time = serializers.DateTimeField(source='date_logged')


    class Meta:
        model = LogData
        fields = '__all__'
