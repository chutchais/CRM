from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Container)

container_detail_url=HyperlinkedIdentityField(
		view_name='container-api:detail',
		lookup_field='number'
		)




class ContainerSerializer(ModelSerializer):
	url =  container_detail_url
	class Meta:
		model = Container
		# fields ='__all__'
		fields = [
			'id',
			'number',
			'url',
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
			'user'
			]


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
			'user'
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
			'status'
			]



