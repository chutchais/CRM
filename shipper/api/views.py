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

from shore.models import Shipper
from .serialize import (ShipperSerializer,
						ShipperDetailSerializer,
						ShipperCreateUpdateSerializer)



class ShipperListAPIView(ListAPIView):
	queryset=Shipper.objects.all()
	serializer_class=ShipperSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['name']
	def get_queryset(self,*args,**kwargs):
		queryset_list =Shipper.objects.all()
		name = self.request.GET.get("name")
		if name != None :
			queryset_list = Shipper.objects.filter(
					Q(name__icontains = name))
		return queryset_list
	# pagination_class = PostPageNumberPagination

class ShipperDetailAPIView(RetrieveAPIView):
	queryset= Shipper.objects.all()
	serializer_class=ShipperDetailSerializer
	lookup_field='slug'
	# print ("vessel details")

class ShipperDeleteAPIView(DestroyAPIView):
	queryset= Shipper.objects.all()
	serializer_class= ShipperDetailSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class ShipperCreateAPIView(CreateAPIView):
	queryset=Shipper.objects.all()
	serializer_class=ShipperCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

# 	def perform_create(self,serializer):
# 		print ('Voy is %s' % self.kwargs.get('voy'))
# 		serializer.save()


