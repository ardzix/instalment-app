# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Wednesday, 10th January 2018 11:38:17 pm
# Last Modified: Thursday, 11th January 2018 12:32:45 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from __future__ import unicode_literals

from django.db import models
from libs.constants import GENDER_CHOICES
from libs.models import BaseModelGeneric, BaseModelUnique
from libs.view import ProtectedMixin
from libs.storages import generate_name, STORAGE_FILE
from django.contrib.auth.models import User
from django.utils import timezone
from libs.moment import to_timestamp
from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Customer(BaseModelUnique):
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, default=3)
    id_num = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    birthday = models.DateField()
    birthplace = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.created_by.first_name, self.created_by.last_name)

    class Meta:
        verbose_name = "Pelanggan"
        verbose_name_plural = "Pelanggan"


class Facility(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Fasilitas"
        verbose_name_plural = "Fasilitas"


class Volume(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    area_wide = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Volume"
        verbose_name_plural = "Volume"


class Witness(BaseModelGeneric):
    fullname = models.CharField(max_length=100)
    id_num = models.CharField(max_length=25)
    address = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = "Saksi"
        verbose_name_plural = "Saksi"


class File(BaseModelGeneric):
    display_name = models.CharField(max_length=100)
    short_name = models.SlugField(max_length=100)
    manager = models.FileField(blank=True, max_length=300, null=True, storage=STORAGE_FILE)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Berkas"
        verbose_name_plural = "Berkas"


class Purchase(BaseModelGeneric):
    customer = models.ForeignKey(Customer, related_name="%(app_label)s_%(class)s_customer")
    volume = models.ForeignKey(Volume, related_name="%(app_label)s_%(class)s_volume")
    witnesses = models.ManyToManyField(Witness, related_name="%(app_label)s_%(class)s_witnesses")
    facilities = models.ManyToManyField(Facility, related_name="%(app_label)s_%(class)s_facilities")
    files = models.ManyToManyField(File, related_name="%(app_label)s_%(class)s_files")
    reg_id = models.CharField(max_length=100)
    reg_behalf = models.CharField(max_length=100)
    area_wide = models.PositiveIntegerField(default=0)
    north_perimeter = models.TextField(blank=True, null=True)
    south_perimeter = models.TextField(blank=True, null=True)
    east_perimeter = models.TextField(blank=True, null=True)
    west_perimeter = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    down_payment = models.PositiveIntegerField(default=0)
    installment_fee = models.PositiveIntegerField(default=0)
    installment_total = models.PositiveIntegerField(default=0)
    due_date = models.PositiveIntegerField(default=0)
    notification_date = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s - %s" % (self.customer.__unicode__(), self.volume.__unicode__())

    class Meta:
        verbose_name = "Berkas"
        verbose_name_plural = "Berkas"


class Installment(BaseModelGeneric):
    purchase = models.ForeignKey(Purchase, related_name="%(app_label)s_%(class)s_purchase")
    customer = models.ForeignKey(Customer, related_name="%(app_label)s_%(class)s_customer")
    files = models.ManyToManyField(File, related_name="%(app_label)s_%(class)s_files")
    order = models.PositiveIntegerField(default=0)
    minus = models.PositiveIntegerField(default=0)
        
    def __unicode__(self):
        return "%s/%s - %s" % (self.order, self.purchase.installment_total(), self.purchase.__unicode__())

    class Meta:
        verbose_name = "Cicilan"
        verbose_name_plural = "Cicilan"

class Finance(BaseModelGeneric):
    description = models.TextField()
    value = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType)
    content_model = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = "Keuangan"
        verbose_name_plural = "Keuangan"