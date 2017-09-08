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

from shore.models import Vessel
from .serialize import (VesselSerializer,
						VesselDetailSerializer,
						VesselCreateUpdateSerializer)



class VesselListAPIView(ListAPIView):
	queryset=Vessel.objects.all()
	serializer_class=VesselSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['number']
	def get_queryset(self,*args,**kwargs):
		queryset_list =Vessel.objects.all()
		name = self.request.GET.get("name")
		if name != None :
			queryset_list = Vessel.objects.filter(
					Q(name__icontains = name))
		return queryset_list
	# pagination_class = PostPageNumberPagination

class VesselDetailAPIView(RetrieveAPIView):
	queryset= Vessel.objects.all()
	serializer_class=VesselDetailSerializer
	lookup_field='slug'
	# print ("vessel details")

class VesselDeleteAPIView(DestroyAPIView):
	queryset= Vessel.objects.all()
	serializer_class= VesselDetailSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class VesselCreateAPIView(CreateAPIView):
	queryset=Vessel.objects.all()
	serializer_class=VesselCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

# 	def perform_create(self,serializer):
# 		print ('Voy is %s' % self.kwargs.get('voy'))
# 		serializer.save()


