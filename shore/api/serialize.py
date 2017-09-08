from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)


from shore.models import (Booking,
							Vessel,
							Shipper)

booking_detail_url=HyperlinkedIdentityField(
		view_name='booking-api:detail',
		lookup_field='number'
		)

class BookingVesselSerializer(ModelSerializer):
	class Meta:
		model = Vessel
		fields =[
			'name',
			'code',
			'description',
		]

class BookingShipperSerializer(ModelSerializer):
	class Meta:
		model = Shipper
		fields =[
			'name',
			'code',
			'description',
		]

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
	# def create(self, validated_data):
	# 	return self.instance

class BookingSerializer(ModelSerializer):
	url = booking_detail_url
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Booking
		# fields ='__all__'
		fields =[
			'id',
			'url',
			'number',
			'voy',
			'pod',
			'shipper',
			'vessel',
			'description',
			'status',
			'created_date',
			'modified_date'
		]



class BookingDetailSerializer(ModelSerializer):
	# vessel = BookingVesselSerializer()
	# shipper = BookingShipperSerializer()
	class Meta:
		model = Booking
		fields =[
			'number',
			'voy',
			'pod',
			'shipper',
			'vessel',
			'description',
			'status',
			'created_date',
			'modified_date'
		]



# class VoySerializer(ModelSerializer):
# 	lov = SerializerMethodField()
# 	vessel_type  = SerializerMethodField()
# 	color = SerializerMethodField()
# 	slug = SerializerMethodField()
# 	startCol = SerializerMethodField()
# 	stopCol = SerializerMethodField()
# 	move_performa = SerializerMethodField()
# 	class Meta:
# 		model = Voy
# 		# fields ='__all__'
# 		fields =['service','vessel','code','voy',
# 				'performa_in','performa_out','eta','etb','etd',
# 				'lov','dis_no','load_no','est_teu',
# 				'terminal','start_pos','vessel_type','color','remark',
# 				'vsl_oper','arrival_draft','departure_draft','slug','draft',
# 				'startCol','stopCol','move_performa','move_confirm','text_pos','qc']

# 	def get_lov(self,obj):
# 		# content_type = obj.get_content_type
# 		# object_id=obj.id
# 		# c_qs = Comment.objects.filter_by_instance(obj)
# 		# comments = CommentSerializer(c_qs,many=True).data
# 		return obj.vessel.lov

# 	def get_vessel_type(self,obj):
# 		return obj.vessel.v_type

# 	def get_color(self,obj):
# 		return obj.service.color

# 	def get_slug(self,obj):
# 		return obj.slug

# 	def get_startCol(self,obj):
# 		return obj.terminal.start_range

# 	def get_stopCol(self,obj):
# 		return obj.terminal.stop_range

# 	def get_move_performa(self,obj):
# 		return obj.service.move_performa


# class VoyDetailSerializer(ModelSerializer):
# 	lov = SerializerMethodField()
# 	vessel_type  = SerializerMethodField()
# 	color = SerializerMethodField()
# 	slug = SerializerMethodField()
# 	startCol = SerializerMethodField()
# 	stopCol = SerializerMethodField()
# 	class Meta:
# 		model = Voy
# 		# fields ='__all__'
# 		fields =['service','vessel','code','voy',
# 				'performa_in','performa_out','eta','etb','etd',
# 				'lov','dis_no','load_no','est_teu',
# 				'terminal','start_pos','vessel_type','color','remark',
# 				'vsl_oper','arrival_draft','departure_draft','slug','draft',
# 				'startCol','stopCol']

# 	def get_lov(self,obj):
# 		# content_type = obj.get_content_type
# 		# object_id=obj.id
# 		# c_qs = Comment.objects.filter_by_instance(obj)
# 		# comments = CommentSerializer(c_qs,many=True).data
# 		return obj.vessel.lov

# 	def get_vessel_type(self,obj):
# 		return obj.vessel.v_type

# 	def get_color(self,obj):
# 		return obj.service.color

# 	def get_slug(self,obj):
# 		return obj.slug

# 	def get_startCol(self,obj):
# 		return obj.terminal.start_range

# 	def get_stopCol(self,obj):
# 		return obj.terminal.stop_range
