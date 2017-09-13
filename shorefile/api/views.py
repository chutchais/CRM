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

from shore.models import ShoreFile
from .serialize import (ShoreFileSerializer,
						ShoreFileDetailSerializer,
						ShoreFileCreateSerializer,
						ShoreFileUpdateSerializer)



class ShoreFileListAPIView(ListAPIView):
	queryset = None #ShoreFile.objects.all()
	serializer_class = ShoreFileSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['name']
	def get_queryset(self,*args,**kwargs):
		queryset_list = None #ShoreFile.objects.all()
		name = self.request.GET.get("name")
		if name != None :
			queryset_list = ShoreFile.objects.filter(
					Q(name__icontains = name))
		return queryset_list
	# pagination_class = PostPageNumberPagination

class ShoreFileDetailAPIView(RetrieveAPIView):
	queryset= ShoreFile.objects.all()
	serializer_class=ShoreFileDetailSerializer
	lookup_field='slug'
	# print ("vessel details")

class ShoreFileDeleteAPIView(DestroyAPIView):
	queryset= ShoreFile.objects.all()
	serializer_class= ShoreFileDetailSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class ShoreFileCreateAPIView(CreateAPIView):
	queryset=ShoreFile.objects.all()
	serializer_class=ShoreFileCreateSerializer
	# def perform_create(self, serializer):
	# 	print ('Now Creating Data')
	# permission_classes = [IsAuthenticated]

class ShoreFileUpdateAPIView(RetrieveUpdateAPIView):
	queryset=ShoreFile.objects.all()
	serializer_class=ShoreFileUpdateSerializer
	lookup_field='slug'
	# permission_classes = [IsAuthenticated]
	# def perform_update(self, serializer):
	# 	print ('Now Updating Data')
	# def perform_update(self, serializer):
 #    instance = serializer.save()
 #    send_email_confirmation(user=self.request.user, modified=instance)

# 	def perform_create(self,serializer):
# 		print ('Voy is %s' % self.kwargs.get('voy'))
# 		serializer.save()


