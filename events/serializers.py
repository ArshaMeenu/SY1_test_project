from rest_framework import  serializers
from app.models import Events



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields= ["event_name","description","end_date","start_date","price"]

