from rest_framework import  serializers
from app.models import Events, UserProfile



class EventSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField(format="%d-%m-%Y")
    start_date =serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Events
        fields= ["id","event_name","description","start_date","end_date","price","is_paid"]


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields= ["user","full_name"]

