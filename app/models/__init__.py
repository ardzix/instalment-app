# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Wednesday, 10th January 2018 11:38:17 pm
# Last Modified: Wednesday, 24th January 2018 10:41:24 am
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
    gender = models.PositiveIntegerField(choices=GENDER_CHOICES, default=3, verbose_name="Nama Tampilan")
    id_num = models.CharField(max_length=25, verbose_name="No ID (KTP/SIM)")
    phone = models.CharField(max_length=25, verbose_name="No Telp")
    birthday = models.DateField(verbose_name="Tanggal Lahir")
    birthplace = models.CharField(max_length=100, verbose_name="Tempat Lahir")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    is_verified = models.BooleanField(default=False, verbose_name="Terverifikasi")

    def __unicode__(self):
        return "%s %s" % (self.created_by.first_name, self.created_by.last_name)

    def get_create_by(self):
        return self.__unicode__()

    class Meta:
        verbose_name = "Pelanggan"
        verbose_name_plural = "Pelanggan"


class Facility(BaseModelGeneric):
    display_name = models.CharField(max_length=100, verbose_name="Nama Tampilan")
    short_name = models.SlugField(max_length=100, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Keterangan")

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Fasilitas"
        verbose_name_plural = "Fasilitas"


class Volume(BaseModelGeneric):
    display_name = models.CharField(max_length=100, verbose_name="Nama Tampilan")
    short_name = models.SlugField(max_length=100, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Keterangan")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    area_wide = models.PositiveIntegerField(default=0, verbose_name="Luas Tanah")

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = "Volume"
        verbose_name_plural = "Volume"


class Witness(BaseModelGeneric):
    fullname = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    id_num = models.CharField(max_length=25, verbose_name="No ID (KTP/SIM)")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")

    def __unicode__(self):
        return self.fullname

    class Meta:
        verbose_name = "Saksi"
        verbose_name_plural = "Saksi"


class File(BaseModelGeneric):
    display_name = models.CharField(max_length=100, verbose_name="Nama Tampinal")
    short_name = models.SlugField(max_length=100, verbose_name="Slug")
    manager = models.FileField(blank=True, max_length=300, null=True, storage=STORAGE_FILE)

    def __unicode__(self):
        return self.display_name

    def get_url(self):
        return self.manager.url

    class Meta:
        verbose_name = "Berkas"
        verbose_name_plural = "Berkas"


class Purchase(BaseModelGeneric):
    customer = models.ForeignKey(Customer, related_name="%(app_label)s_%(class)s_customer", verbose_name="Pelanggan")
    volume = models.ForeignKey(Volume, related_name="%(app_label)s_%(class)s_volume")
    witnesses = models.ManyToManyField(Witness, related_name="%(app_label)s_%(class)s_witnesses", verbose_name="Saksi")
    facilities = models.ManyToManyField(Facility, related_name="%(app_label)s_%(class)s_facilities", verbose_name="Fasilitas")
    files = models.ManyToManyField(File, related_name="%(app_label)s_%(class)s_files", verbose_name="Berkas")
    reg_id = models.CharField(max_length=100, verbose_name="No Induk Akte")
    reg_behalf = models.CharField(max_length=100, verbose_name="Akte Atas Nama")
    area_wide = models.PositiveIntegerField(default=0, verbose_name="Luas Tanah")
    north_perimeter = models.TextField(blank=True, null=True, verbose_name="Batas Utara")
    south_perimeter = models.TextField(blank=True, null=True, verbose_name="Batas Selatan")
    east_perimeter = models.TextField(blank=True, null=True, verbose_name="Batas Timur")
    west_perimeter = models.TextField(blank=True, null=True, verbose_name="Batas Barat")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    down_payment = models.PositiveIntegerField(default=0, verbose_name="Uang Muka")
    installment_fee = models.PositiveIntegerField(default=0, verbose_name="Biaya Cicilan")
    installment_total = models.PositiveIntegerField(default=0, verbose_name="Total Cicilan")
    due_date = models.PositiveIntegerField(default=0, verbose_name="Jatuh Tempo")
    notification_date = models.PositiveIntegerField(default=0, verbose_name="Tanggal Pengingat")

    def __unicode__(self):
        return "%s - %s" % (self.customer.__unicode__(), self.volume.__unicode__())

    class Meta:
        verbose_name = "Pembelian"
        verbose_name_plural = "Pembelian"


class Installment(BaseModelGeneric):
    purchase = models.ForeignKey(Purchase, related_name="%(app_label)s_%(class)s_purchase", verbose_name="Pembelian")
    customer = models.ForeignKey(Customer, related_name="%(app_label)s_%(class)s_customer", verbose_name="Pelanggan")
    files = models.ManyToManyField(File, related_name="%(app_label)s_%(class)s_files", verbose_name="Berkas")
    order = models.PositiveIntegerField(default=0, verbose_name="Cicilan Ke")
    minus = models.PositiveIntegerField(default=0, verbose_name="Kekurangan")
        
    def __unicode__(self):
        return "%s/%s - %s" % (self.order, self.purchase.installment_total, self.purchase.__unicode__())

    class Meta:
        verbose_name = "Cicilan"
        verbose_name_plural = "Cicilan"


class Finance(BaseModelGeneric):
    description = models.TextField(verbose_name="Keterangan")
    value = models.IntegerField(default=0, verbose_name="Nilai")
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    content_model = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = "Keuangan"
        verbose_name_plural = "Keuangan"