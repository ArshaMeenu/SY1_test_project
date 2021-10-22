from rest_framework import  serializers
from app.models import Events, UserProfile
from django_countries.serializers import CountryFieldMixin




class EventSerializer(CountryFieldMixin,serializers.ModelSerializer):
    end_date = serializers.DateField(format="%d-%m-%Y")
    start_date =serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Events
        fields= ["id","event_name","description","start_date","end_date","price","is_paid","country"]

    
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = "user.username")
    
    class Meta:
        model = UserProfile
        fields= ["user","full_name"]

