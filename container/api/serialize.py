from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Container)
from booking.api.serialize import BookingSerializer

container_detail_url=HyperlinkedIdentityField(
		view_name='container-api:detail',
		lookup_field='slug'
		)




class ContainerSerializer(ModelSerializer):
	url =  container_detail_url
	booking = BookingSerializer()
	class Meta:
		model = Container
		# fields ='__all__'
		fields = [
			'id',
			'number',
			'url',
			'container_type',
			'container_size',
			'container_high',
			'description',
			'payment',
			'dg_class',
			'unno',
			'temperature',
			'status',
			'created_date',
			'modified_date',
			'booking',
			'user',
			'draft',
			'slug'
			]
	def create(self, validated_data):
		print ('Create on Rest')
		return Container(**validated_data)

	def update(self, instance, validated_data):
		print ('Update on Rest')
		return instance


class ContainerDetailSerializer(ModelSerializer):
	class Meta:
		model = Container
		# fields ='__all__'
		fields = [
			'id',
			'number',
			'container_type',
			'container_size',
			'description',
			'payment',
			'dg_class',
			'unno',
			'temperature',
			'status',
			'created_date',
			'modified_date',
			'booking',
			'user',
			'draft',
			'slug'
			]

class ContainerCreateUpdateSerializer (ModelSerializer):
	class Meta:
		model = Container
		fields = [
			'number',
			'booking',
			'container_type',
			'container_size',
			'description',
			'payment',
			'dg_class',
			'unno',
			'temperature',
			'status',
			'upload_status',
			'upload_date',
			'upload_msg',
			'draft'
			]
	# def create(self, validated_data):
	# 	print ('Create on Rest')
	# 	return Container(**validated_data)

	# def update(self, instance, validated_data):
	# 	print ('Update on Rest')
	# 	return instance



