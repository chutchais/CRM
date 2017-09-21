from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )


class FileType(models.Model):
	name = models.CharField(max_length=50,primary_key=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	line_col  = models.CharField(max_length=50,blank=True, null=True)
	line_default  = models.CharField(verbose_name ='LINE default value',max_length=50,blank=True, null=True)
	agent_col  = models.CharField(max_length=50,blank=True, null=True)
	agent_default  = models.CharField(verbose_name ='Agent default value',max_length=50,blank=True, null=True)
	shipper_col  = models.CharField(max_length=50,blank=True, null=True)
	vessel_col  = models.CharField(max_length=50,blank=True, null=True)
	voy_col  = models.CharField(max_length=50,blank=True, null=True)
	booking_col  = models.CharField(max_length=50,blank=True, null=True)
	container_col  = models.CharField(max_length=50,blank=True, null=True)
	container_type_col  = models.CharField(max_length=50,blank=True, null=True)
	container_size_col  = models.CharField(max_length=50,blank=True, null=True)
	container_high_col  = models.CharField(max_length=50,blank=True, null=True)
	pod_col  = models.CharField(max_length=50,blank=True, null=True)
	payment_col  = models.CharField(max_length=50,blank=True, null=True)
	dgclass_col  = models.CharField(max_length=50,blank=True, null=True)
	unno_col  = models.CharField(max_length=50,blank=True, null=True)
	stowage_col  = models.CharField(max_length=50,blank=True, null=True)
	temp_col  = models.CharField(max_length=50,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name



class ShoreFile(models.Model):
	name = models.CharField(max_length=100,primary_key=True)
	filename = models.FileField(upload_to='shores/%Y/%m/%d/',blank=True, null=True)
	filetype =  models.ForeignKey('FileType', related_name='shorefiles',blank=True, null=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=DEACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	upload_status = models.NullBooleanField(verbose_name ='Upload Status')
	upload_date = models.DateTimeField(blank=True, null=True)
	upload_msg = models.CharField(max_length=255,blank=True, null=True)
	
	def __str__(self):
		return self.name
	
	def item_count(self):
		return self.containers.count()

	def uploaded_count(self):
		return self.containers.filter(upload_status__isnull = False).count()

	class Meta:
		ordering = ('-created_date',)

class Vessel(models.Model):
	name = models.CharField(verbose_name ='Feeder Vessel',max_length=50)
	code = models.CharField(verbose_name ='Feeder Vessel Code',max_length=30)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

class Shipper(models.Model):
	name = models.CharField(verbose_name ='Shipper Name',max_length=50)
	code = models.CharField(verbose_name ='Shipper Code',max_length=30,blank=True, null=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

class Booking(models.Model):
	number = models.CharField(verbose_name ='Booking Number',max_length=50)
	slug = models.SlugField(unique=True,blank=True, null=True)
	voy = models.CharField(verbose_name ='Voyage',max_length=50,blank=True, null=True)
	pod = models.CharField(verbose_name ='Port Of Destination',max_length=50,blank=True, null=True)
	line = models.CharField(verbose_name ='Line',max_length=50,blank=True, null=True)
	agent = models.CharField(verbose_name ='Agent',max_length=50,blank=True, null=True)
	shipper  = models.ForeignKey('Shipper', related_name='bookings',blank=True, null=True)
	vessel  = models.ForeignKey('Vessel', related_name='bookings')
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.number

class Container(models.Model):
	number = models.CharField(max_length=50,blank=False, null=False)
	slug = models.SlugField(unique=True,blank=True, null=True)
	booking  = models.ForeignKey('Booking', related_name='containers')
	container_type = models.CharField(max_length=10,default='DV')
	container_size = models.CharField(max_length=10,blank=True, null=True ,default='20')
	container_high = models.CharField(max_length=10,blank=True, null=True ,default='8.6')
	description = models.CharField(max_length=255,blank=True, null=True)
	payment = models.CharField(verbose_name ='Payment(Cash)',max_length=10,blank=True, null=True ,default='CASH')
	dg_class =  models.CharField(max_length=10,blank=True, null=True)
	unno =  models.CharField(max_length=20,blank=True, null=True)
	temperature = models.FloatField(default=20)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	draft = models.BooleanField(verbose_name ='Save as draft',default=False)
	upload_status = models.NullBooleanField(verbose_name ='Upload Success')
	upload_date = models.DateTimeField(blank=True, null=True)
	upload_msg = models.CharField(max_length=255,blank=True, null=True)
	shorefile  = models.ForeignKey('ShoreFile', related_name='containers',blank=True, null=True)
	
	def __str__(self):
		return self.number





# Slug Hadeling#
def create_shipper_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Shipper.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_shipper_slug(instance, new_slug=new_slug)
    return slug

def pre_save_shipper_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_shipper_slug(instance)
pre_save.connect(pre_save_shipper_receiver, sender=Shipper)


def create_vessel_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Vessel.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_vessel_slug(instance, new_slug=new_slug)
    return slug

def pre_save_vessel_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_vessel_slug(instance)
pre_save.connect(pre_save_vessel_receiver, sender=Vessel)


def create_booking_slug(instance, new_slug=None):
    slug = slugify(instance.number)
    if new_slug is not None:
        slug = new_slug
    qs = Booking.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s-%s" %(slug, qs.first().voy ,qs.first().pod)
        return create_booking_slug(instance, new_slug=new_slug)
    return slug

def pre_save_booking_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_booking_slug(instance)
pre_save.connect(pre_save_booking_receiver, sender=Booking)

def create_shorefile_slug(instance, new_slug=None):
    import datetime
    slug = slugify(instance.name)
    print ('New slug %s' % slug)
    if new_slug is not None:
        slug = new_slug
    qs = ShoreFile.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        # new_slug = "%s-%s" %(slug, qs.first().id)
        new_slug = "%s-%s" %(slug, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
        print ('New slug %s' % new_slug)
        return create_shorefile_slug(instance, new_slug=new_slug)
    return slug

def pre_save_shorefile_receiver(sender, instance, *args, **kwargs):
	# print ('Presave Trigger')
	#To support Save as Draft 
	# instance.slug = create_shorefile_slug(instance)
	if not instance.slug:
		instance.slug = create_shorefile_slug(instance)

pre_save.connect(pre_save_shorefile_receiver, sender=ShoreFile)


def create_container_slug(instance, new_slug=None):
    import datetime
    slug = slugify(instance.number)
    if new_slug is not None:
        slug = new_slug
    qs = Container.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        # new_slug = "%s-%s" %(slug, qs.first().id)
        new_slug = "%s-%s" %(slug,instance.booking )
        return create_container_slug(instance, new_slug=new_slug)
    return slug

def pre_save_container_receiver(sender, instance, *args, **kwargs):
	# print ('Presave Trigger')
	#To support Save as Draft 
	# instance.slug = create_shorefile_slug(instance)
	if not instance.slug:
		instance.slug = create_container_slug(instance)

pre_save.connect(pre_save_container_receiver, sender=Container)