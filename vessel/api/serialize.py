from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Booking,
							Vessel,
							Shipper)

vessel_detail_url=HyperlinkedIdentityField(
		view_name='vessel-api:detail',
		lookup_field='slug'
		)


class VesselCreateUpdateSerializer (ModelSerializer):
	class Meta:
		model = Vessel
		fields =[
			'name',
			'code',
			'description'
		]


class VesselListSerializer(ModelSerializer):
	# url = vessel_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Vessel
		# fields ='__all__'
		fields = [
			'name',
			'code',
			]

class VesselSerializer(ModelSerializer):
	url = vessel_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Vessel
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


class VesselDetailSerializer(ModelSerializer):
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Vessel
		fields ='__all__'




