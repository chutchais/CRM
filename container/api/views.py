from django.db.models import Q

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView
	)

from rest_framework import status , generics , mixins

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
	search_fields =['slug']
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
	lookup_field='slug'
	# print ("vessel details")

class ContainerDeleteAPIView(DestroyAPIView):
	queryset= Container.objects.all()
	serializer_class= ContainerDetailSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class ContainerCreateAPIView(CreateAPIView):
	queryset=Container.objects.all()
	serializer_class=ContainerCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

class ContainerUpdateAPIView(RetrieveUpdateDestroyAPIView):
	queryset= Container.objects.all()
	serializer_class= ContainerCreateUpdateSerializer
	lookup_field='slug'
	print('On ContainerUpdateAPIView')



	# def update(self, request, *args, **kwargs):
	# 	print('Hit Update function')
	# 	instance = self.get_object()
	# 	instance.name = request.data.get("name")
	# 	instance.save()

	# 	partial = kwargs.pop('partial', False)
	# 	serializer = self.get_serializer(instance,data=request.data, partial=partial)
	# 	serializer.is_valid(raise_exception=True)
	# 	self.perform_update(serializer)

	# 	return Response(serializer.data)



