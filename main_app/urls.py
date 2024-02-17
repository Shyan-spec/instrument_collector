from django.urls import path
from .views import Home, InstrumentsView, InstrumentsDetail, RenterListCreate, RenterDetails, CollectionsCreateList, CollectionDetails, AddInstrumentToCollection, LoginView, VerifyUserView, CreateUserView


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('instruments/', InstrumentsView.as_view(), name='instruments-view'),
  path('instruments/<int:id>/', InstrumentsDetail.as_view(), name='instruments-detail'),
  path('instruments/<int:instrument_id>/renters/', RenterListCreate.as_view(), name='Renter-list-create'),
  path('instruments/<int:instrument_id>/renters/<int:id>/', RenterDetails.as_view(), name='Renter-details'),
  path('collections/', CollectionsCreateList.as_view(), name='collections-create-list'),
  path('collections/<int:id>/', CollectionDetails.as_view(), name='collection-details'),
  path('collections/<int:collection_id>/add_instrument/<int:instrument_id>/', AddInstrumentToCollection.as_view(), name='add-instruments-to-collections'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]