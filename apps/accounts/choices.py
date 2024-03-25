from django.db import models


class UserField(models.TextChoices):
    BILLBOARD_OWNER = 'billboard-owner'
    STATE_AGENT = 'state-agent'
    ADVERTISING_AGENT = 'advertising-agent'
    BUSINESS_OWNER = 'business-owner'


class Country(models.TextChoices):
    NIGERIA = 'NG'


class State(models.TextChoices):
    ABIA = 'abia'
    ADAMAWA = 'adamawa'
    AKWA_IBOM = 'akwa-ibom'
    ANAMBRA = 'anambra'
    BAUCHI = 'bauchi'
    BAYELSA = 'bayelsa'
    BENUE = 'benue'
    BORNO = 'borno'
    CROSS_RIVER = 'cross-river'
    DELTA = 'delta'
    EBONYI = 'ebonyi'
    EDO = 'edo'
    EKITI = 'ekiti'
    ENUGU = 'enugu'
    FCT = 'fct'
    GOMBE = 'gombe'
    IMO = 'imo'
    JIGAWA = 'jigawa'
    KADUNA = 'kaduna'
    KANO = 'kano'
    KATSINA = 'katsina'
    KEBBI = 'kebbi'
    KOGI = 'kogi'
    KWARA = 'kwara'
    LAGOS = 'lagos'
    NASARAWA = 'nasarawa'
    NIGER = 'niger'
    OGUN = 'ogun'
    ONDO = 'ondo'
    OSUN = 'osun'
    OYO = 'oyo'
    PLATEAU = 'plateau'
    RIVERS = 'rivers'
    SOKOTO = 'sokoto'
    TARABA = 'taraba'
    YOBE = 'yobe'
    ZAMFARA = 'zamfara'
