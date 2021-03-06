from django.db.models import Q

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

# from .serialize import VoySerializer,VoyDetailSerializer
# from berth.models import Voy

from shore.models import Booking
from .serialize import (BookingSerializer,
						BookingDetailSerializer,
						BookingCreateUpdateSerializer)



class BookingListAPIView(ListAPIView):
	queryset = None #Booking.objects.all()
	serializer_class = BookingSerializer
	filter_backends = [SearchFilter,OrderingFilter]
	search_fields = ['number']
	def get_queryset(self,*args,**kwargs):
		queryset_list =None #Booking.objects.all()
		number = self.request.GET.get("number")
		if number != None :
			queryset_list = Booking.objects.filter(
					Q(number__icontains = number))
		return queryset_list
	# pagination_class = PostPageNumberPagination

class BookingDetailAPIView(RetrieveAPIView):
	queryset= Booking.objects.all()
	serializer_class = BookingDetailSerializer
	lookup_field = 'slug'
	# print ("vessel details")

class BookingDeleteAPIView(DestroyAPIView):
	queryset= Booking.objects.all()
	serializer_class= BookingDetailSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class BookingCreateAPIView(CreateAPIView):
	queryset= Booking.objects.all()
	serializer_class= BookingCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

# 	def perform_create(self,serializer):
# 		print ('Voy is %s' % self.kwargs.get('voy'))
# 		serializer.save()


