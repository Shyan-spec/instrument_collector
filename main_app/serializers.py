from rest_framework import serializers
from .models import Instruments, Renter, Collections
from django.contrib.auth.models import User

class InstrumentsSerializer(serializers.ModelSerializer):
     user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make the user field read-only
     class Meta:
        model = Instruments
        fields = '__all__'
        
class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = '__all__'
        
class RenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = '__all__'
        read_only_fields=('instrument',)
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user