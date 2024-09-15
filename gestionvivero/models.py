from django.db import models

# Modelo Productor
class Productor(models.Model):
    """
    El modelo `Productor` representa a un productor de viveros.
    Este modelo almacena información personal relevante del productor.
    
    Campos:
    - documento_identidad (CharField): Número de documento de identidad del productor. Debe ser único.
    - nombre (CharField): Nombre del productor.
    - apellido (CharField): Apellido del productor.
    - telefono (CharField): Número de teléfono del productor.
    - correo (EmailField): Correo electrónico del productor.
    
    Métodos:
    - __str__(): Retorna una representación en cadena del productor en el formato `Nombre Apellido`.
    """
    documento_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

# Modelo Finca
class Finca(models.Model):
    """
    El modelo `Finca` representa una finca que pertenece a un productor.
    Cada finca tiene un número de catastro y una ubicación municipal.
    
    Campos:
    - productor (ForeignKey): Relación de muchos a uno con el modelo `Productor`. Indica el productor al que pertenece la finca.
    - numero_catastro (CharField): Número de catastro de la finca. Debe ser único.
    - municipio (CharField): Municipio en el que se encuentra la finca.
    
    Métodos:
    - __str__(): Retorna una representación en cadena de la finca en el formato `Finca Número de Catastro - Municipio`.
    """
    productor = models.ForeignKey(Productor, on_delete=models.CASCADE, related_name='fincas')
    numero_catastro = models.CharField(max_length=50, unique=True)
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return f'Finca {self.numero_catastro} - {self.municipio}'

# Modelo Vivero
class Vivero(models.Model):
    """
    El modelo `Vivero` representa un vivero dentro de una finca.
    Cada vivero tiene un código y un tipo de cultivo.
    
    Campos:
    - finca (ForeignKey): Relación de muchos a uno con el modelo `Finca`. Indica la finca a la que pertenece el vivero.
    - codigo (CharField): Código asignado al vivero.
    - tipo_cultivo (CharField): Tipo de cultivo en el vivero.
    
    Métodos:
    - __str__(): Retorna una representación en cadena del vivero en el formato `Vivero Código - Tipo de Cultivo`.
    """
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, related_name='viveros')
    codigo = models.CharField(max_length=50, unique=True)  # Asegúrate de que unique=True esté presente
    tipo_cultivo = models.CharField(max_length=100)

    def __str__(self):
        return f'Vivero {self.codigo} - {self.tipo_cultivo}'

# Clase abstracta ProductoControl
class ProductoControl(models.Model):
    """
    La clase abstracta `ProductoControl` define los atributos comunes para todos los productos de control.
    Esta clase no se puede instanciar directamente, pero proporciona una base para los modelos que la extienden.
    
    Campos:
    - registro_ica (CharField): Registro ICA del producto.
    - nombre_producto (CharField): Nombre del producto.
    - frecuencia_aplicacion (IntegerField): Frecuencia de aplicación del producto (cada cuántos días).
    - valor (DecimalField): Valor del producto.
    
    Clase Meta:
    - abstract (True): Indica que esta clase es abstracta y no debe ser creada directamente.
    """
    registro_ica = models.CharField(max_length=50)
    nombre_producto = models.CharField(max_length=100)
    frecuencia_aplicacion = models.IntegerField()  # Cada X días
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

# Modelo ProductoControlHongo
class ProductoControlHongo(ProductoControl):
    """
    El modelo `ProductoControlHongo` extiende `ProductoControl` para representar productos de control específicos para hongos.
    
    Campos:
    - periodo_carencia (IntegerField): Número de días que debe transcurrir entre la última aplicación y la cosecha.
    - nombre_hongo (CharField): Nombre del hongo que afecta la planta.
    
    Métodos:
    - __str__(): Retorna una representación en cadena del producto de control de hongo en el formato `Hongo Nombre del Hongo - Nombre del Producto`.
    """
    periodo_carencia = models.IntegerField()  # Días
    nombre_hongo = models.CharField(max_length=100)

    def __str__(self):
        return f'Hongo {self.nombre_hongo} - {self.nombre_producto}'

# Modelo ProductoControlPlaga
class ProductoControlPlaga(ProductoControl):
    """
    El modelo `ProductoControlPlaga` extiende `ProductoControl` para representar productos de control específicos para plagas.
    
    Campos:
    - periodo_carencia (IntegerField): Número de días que debe transcurrir entre la última aplicación y la cosecha.
    
    Métodos:
    - __str__(): Retorna una representación en cadena del producto de control de plaga en el formato `Plaga - Nombre del Producto`.
    """
    periodo_carencia = models.IntegerField()  # Días

    def __str__(self):
        return f'Plaga - {self.nombre_producto}'

# Modelo ProductoControlFertilizante
class ProductoControlFertilizante(ProductoControl):
    """
    El modelo `ProductoControlFertilizante` extiende `ProductoControl` para representar productos de fertilización.
    
    Campos:
    - fecha_ultima_aplicacion (DateField): Fecha de la última aplicación del fertilizante.
    
    Métodos:
    - __str__(): Retorna una representación en cadena del producto de control de fertilizante en el formato `Fertilizante - Nombre del Producto`.
    """
    fecha_ultima_aplicacion = models.DateField()

    def __str__(self):
        return f'Fertilizante - {self.nombre_producto}'

# Modelo Labor
class Labor(models.Model):
    """
    El modelo `Labor` representa una labor realizada en un vivero.
    Cada labor tiene una fecha y una descripción, y puede utilizar varios productos de control.
    
    Campos:
    - vivero (ForeignKey): Relación de muchos a uno con el modelo `Vivero`. Indica el vivero en el que se realiza la labor.
    - fecha (DateField): Fecha en la que se realiza la labor.
    - descripcion (TextField): Descripción de la labor realizada.
    - productos_control_hongo (ManyToManyField): Relación de muchos a muchos con `ProductoControlHongo`. Los productos de control de hongos utilizados en la labor.
    - productos_control_plaga (ManyToManyField): Relación de muchos a muchos con `ProductoControlPlaga`. Los productos de control de plagas utilizados en la labor.
    - productos_control_fertilizante (ManyToManyField): Relación de muchos a muchos con `ProductoControlFertilizante`. Los productos de fertilización utilizados en la labor.
    
    Métodos:
    - __str__(): Retorna una representación en cadena de la labor en el formato `Labor Descripción en Fecha`.
    """
    vivero = models.ForeignKey(Vivero, on_delete=models.CASCADE, related_name='labores')
    fecha = models.DateField()
    descripcion = models.TextField()

    # Relacionamos Labor con los productos que puede utilizar
    productos_control_hongo = models.ManyToManyField(ProductoControlHongo)
    productos_control_plaga = models.ManyToManyField(ProductoControlPlaga)
    productos_control_fertilizante = models.ManyToManyField(ProductoControlFertilizante)

    def __str__(self):
        return f'Labor {self.descripcion} en {self.fecha}'
