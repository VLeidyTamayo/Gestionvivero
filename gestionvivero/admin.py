from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Productor, Finca, Vivero, ProductoControlHongo, ProductoControlPlaga, ProductoControlFertilizante, Labor

@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):
    list_display = ('documento_identidad', 'nombre', 'apellido', 'telefono', 'correo')

@admin.register(Finca)
class FincaAdmin(admin.ModelAdmin):
    list_display = ('productor', 'numero_catastro', 'municipio')

@admin.register(Vivero)
class ViveroAdmin(admin.ModelAdmin):
    list_display = ('finca', 'codigo', 'tipo_cultivo')

@admin.register(ProductoControlHongo)
class ProductoControlHongoAdmin(admin.ModelAdmin):
    list_display = ('registro_ica', 'nombre_producto', 'frecuencia_aplicacion', 'valor', 'periodo_carencia', 'nombre_hongo')

@admin.register(ProductoControlPlaga)
class ProductoControlPlagaAdmin(admin.ModelAdmin):
    list_display = ('registro_ica', 'nombre_producto', 'frecuencia_aplicacion', 'valor', 'periodo_carencia')

@admin.register(ProductoControlFertilizante)
class ProductoControlFertilizanteAdmin(admin.ModelAdmin):
    list_display = ('registro_ica', 'nombre_producto', 'frecuencia_aplicacion', 'valor', 'fecha_ultima_aplicacion')

@admin.register(Labor)
class LaborAdmin(admin.ModelAdmin):
    list_display = ('vivero', 'fecha', 'descripcion')
    filter_horizontal = ('productos_control_hongo', 'productos_control_plaga', 'productos_control_fertilizante')
