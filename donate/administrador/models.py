# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Block(models.Model):
    idblock = models.IntegerField(primary_key=True)
    hash = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.CharField(max_length=45, blank=True, null=True)
    transaccion_idtransaccion = models.ForeignKey('Transaccion', models.DO_NOTHING, db_column='transaccion_idtransaccion')

    class Meta:
        managed = False
        db_table = 'block'


class CausasBeneficas(models.Model):
    idcausas_beneficas = models.IntegerField(primary_key=True)
    nombre_causa = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'causas_beneficas'


class EstadoDonacion(models.Model):
    idestado_donacion = models.IntegerField(primary_key=True)
    estado_donacioncol = models.CharField(max_length=45, blank=True, null=True)
    descripcion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_donacion'


class Transaccion(models.Model):
    idtransaccion = models.IntegerField(primary_key=True)
    monto = models.CharField(max_length=45, blank=True, null=True)
    timestamp = models.CharField(max_length=45, blank=True, null=True)
    wallet_idwallet = models.ForeignKey('Wallet', models.DO_NOTHING, db_column='wallet_idwallet')
    causas_beneficas_idcausas_beneficas = models.ForeignKey(CausasBeneficas, models.DO_NOTHING, db_column='causas_beneficas_idcausas_beneficas')
    estado_donacion_idestado_donacion = models.ForeignKey(EstadoDonacion, models.DO_NOTHING, db_column='estado_donacion_idestado_donacion')
    usuario_idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_idusuario')

    class Meta:
        managed = False
        db_table = 'transaccion'


class Usuario(models.Model):
    idusuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    monto = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Wallet(models.Model):
    idwallet = models.IntegerField(primary_key=True)
    balance = models.CharField(max_length=45, blank=True, null=True)
    direccion = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wallet'
