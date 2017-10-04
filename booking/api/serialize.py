from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Booking)
from shipper.api.serialize import ShipperSerializer,ShipperListSerializer
from vessel.api.serialize import VesselSerializer,VesselListSerializer

booking_detail_url=HyperlinkedIdentityField(
		view_name='booking-api:detail',
		lookup_field='slug'
		)


# class BookingCreateUpdateSerializer (ModelSerializer):
# 	class Meta:
# 		model = Booking
# 		fields =[
# 			'number',
# 			'code',
# 			'description'
# 		]

class BookingCreateUpdateSerializer (ModelSerializer):
	class Meta:
		model = Booking
		fields =[
			'number',
			'voy',
			'vessel',
			'pod',
			'shipper',
			'description'
		]

class BookingListSerializer(ModelSerializer):
	# url = booking_detail_url
	# shipper = ShipperListSerializer(allow_null=True)
	# vessel = VesselListSerializer()
	class Meta:
		model = Booking
		# fields ='__all__'
		fields = [
			'number',
			'line',
			'agent',
			'voy',
			# 'vessel',
			'pod',
			# 'shipper',
			]

class BookingSerializer(ModelSerializer):
	# url = booking_detail_url
	shipper = ShipperSerializer(allow_null=True)
	vessel = VesselSerializer()
	class Meta:
		model = Booking
		# fields ='__all__'
		fields = [
			'id',
			'number',
			# 'url',
			'slug',
			'line',
			'agent',
			'voy',
			'vessel',
			'pod',
			'shipper',
			'description',
			'status',
			'created_date',
			'user'
			]


class BookingDetailSerializer(ModelSerializer):
	# url = booking_detail_url
	class Meta:
		model = Booking
		fields = [
			'id',
			'number',
			# 'url',
			'slug',
			'line',
			'agent',
			'voy',
			'pod',
			'description',
			'status',
			'created_date',
			'user'
			]




