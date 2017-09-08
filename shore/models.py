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
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name

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
	shipper  = models.ForeignKey('Shipper', related_name='bookings')
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
	booking  = models.ForeignKey('Booking', related_name='containers')
	container_type = models.CharField(max_length=10,default='DV')
	container_size = models.CharField(max_length=10,blank=True, null=True ,default='20')
	container_high = models.CharField(max_length=10,blank=True, null=True ,default='8.6')
	description = models.CharField(max_length=255,blank=True, null=True)
	payment = models.CharField(max_length=10,blank=True, null=True ,default='CASH')
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