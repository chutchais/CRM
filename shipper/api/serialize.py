from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Booking,
							Vessel,
							Shipper)

shipper_detail_url=HyperlinkedIdentityField(
		view_name='shipper-api:detail',
		lookup_field='slug'
		)


class ShipperCreateUpdateSerializer (ModelSerializer):
	class Meta:
		model = Shipper
		fields =[
			'name',
			'code',
			'description'
		]

class ShipperListSerializer(ModelSerializer):
	# url = shipper_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Shipper
		# fields ='__all__'
		fields = [
			'name',
			]

class ShipperSerializer(ModelSerializer):
	url = shipper_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Shipper
		# fields ='__all__'
		fields = [
			'id',
			'name',
			'url',
			'slug',
			'code',
			'description',
			'status',
			'created_date',
			'user'
			]


class ShipperDetailSerializer(ModelSerializer):
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Shipper
		fields ='__all__'




