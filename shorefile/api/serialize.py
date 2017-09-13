from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (ShoreFile)

shorefile_detail_url=HyperlinkedIdentityField(
		view_name='shorefile-api:detail',
		lookup_field='slug'
		)


class ShoreFileCreateSerializer (ModelSerializer):
	url = shorefile_detail_url
	class Meta:
		model = ShoreFile
		fields =[
			'name',
			'filename',
			'filetype',
			'url',
			'description',
			'status',
			'upload_status',
			'upload_date',
			'upload_msg'
		]

class ShoreFileUpdateSerializer (ModelSerializer):
	class Meta:
		model = ShoreFile
		fields =[
			'description',
			'status',
			'upload_status',
			'upload_date',
			'upload_msg'
		]

	# def update(self, instance, validated_data):
	# 	print ('this - here')
	# 	return None
        # demo = Demo.objects.get(pk=instance.id)
        # Demo.objects.filter(pk=instance.id)\
        #                    .update(**validated_data)
        # return demo


class ShoreFileSerializer(ModelSerializer):
	url = shorefile_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = ShoreFile
		# fields ='__all__'
		fields = [
			'name',
			'filename',
			'filetype',
			'url',
			'slug',
			'description',
			'status',
			'created_date',
			'user',
			'upload_status',
			'upload_date',
			'upload_msg'
			]


class ShoreFileDetailSerializer(ModelSerializer):
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = ShoreFile
		fields ='__all__'




