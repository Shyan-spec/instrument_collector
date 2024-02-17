from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .serializers import InstrumentsSerializer, RenterSerializer, CollectionsSerializer, UserSerializer 
from .models import Instruments, Renter,Collections
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the instrument-collector api home route!'}
    return Response(content)

class InstrumentsView(generics.ListCreateAPIView):
    queryset = Instruments.objects.all()
    serializer_class = InstrumentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
      # This ensures we only return instruments belonging to the logged-in user
      user = self.request.user
      return Instruments.objects.filter(user=user)

    def perform_create(self, serializer):
      # This associates the newly created instrument with the logged-in user
      serializer.save(user=self.request.user)
    
    

class InstrumentsDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Instruments.objects.all()
  serializer_class = InstrumentsSerializer
  lookup_field = 'id'
  
  def get_queryset(self):
    user = self.request.user
    return Instruments.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    instruments_not_associated = Renter.objects.exclude(id__in=instance.toys.all())
    renter_serializer = RenterSerializer(instruments_not_associated, many=True)

    
    return Response({
        'instrument': serializer.data,
        'instruments_not_associated': render_serializer.data
    })
    
  def perform_update(self, serializer):
      instrument = self.get_object()
      if instrument.user != self.request.user:
          raise PermissionDenied({"message": "You do not have permission to edit this instrument."})
      serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this instrument."})
    instance.delete()

  
class RenterListCreate(generics.ListCreateAPIView):
    serializer_class = RenterSerializer

    def get_queryset(self):
        instrument_id = self.kwargs['instrument_id']
        return Renter.objects.filter(instrument_id=instrument_id)

    def perform_create(self, serializer):
        instrument_id = self.kwargs['instrument_id']
        instrument = get_object_or_404(Instruments, id=instrument_id)  # Corrected to fetch Instrument
        serializer.save(instrument=instrument)

class RenterDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RenterSerializer
    lookup_field = 'id'

    def get_queryset(self):
        instrument_id = self.kwargs['instrument_id']  # For consistency
        return Renter.objects.filter(instrument_id=instrument_id)
    
class CollectionsCreateList(generics.ListCreateAPIView):
    queryset = Collections.objects.all()
    serializer_class=CollectionsSerializer

class CollectionDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset= Collections.objects.all()
    serializer_class=CollectionsSerializer
    lookup_field = 'id'
    
class AddInstrumentToCollection(APIView):
    def post(self, request, instrument_id, collection_id):
        instrument= Instruments.objects.get(id=instrument_id)
        collection= Collections.objects.get(id=collection_id)
        collection.toys.add(instrument)
        return Response({'message': f'Instrument {instrument.name} added to Collection {collection.name}'})
  
        