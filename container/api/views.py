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
from shore.models import Booking

from shore.models import Container
from .serialize import (ContainerSerializer,
						ContainerDetailSerializer,
						ContainerCreateUpdateSerializer)



class ContainerListAPIView(ListAPIView):
	queryset = Container.objects.all()
	serializer_class= ContainerSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['number']
	def get_queryset(self,*args,**kwargs):
		queryset_list = None#Container.objects.all()
		number = self.request.GET.get("number")
		booking = self.request.GET.get("booking")
		draft = self.request.GET.get("draft")
		if number != None and booking == None :
			queryset_list = Container.objects.filter(
					Q(number__icontains = number),draft=False )
		if number != None and booking !=None :
			b = Booking.objects.filter(number=booking)
			if b == None:
				queryset_list = None
			else:
				queryset_list = Container.objects.filter(
						Q(number__icontains = number) &
						Q(booking = b.first()),draft=False)
		if draft == 'true':
			queryset_list = Container.objects.filter(draft=True)

		return queryset_list
	# pagination_class = PostPageNumberPagination

class ContainerDetailAPIView(RetrieveAPIView):
	queryset= Container.objects.all()
	serializer_class= ContainerDetailSerializer
	lookup_field='number'
	# print ("vessel details")

class ContainerDeleteAPIView(DestroyAPIView):
	queryset= Container.objects.all()
	serializer_class= ContainerDetailSerializer
	lookup_field='number'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class ContainerCreateAPIView(CreateAPIView):
	queryset=Container.objects.all()
	serializer_class=ContainerCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]



