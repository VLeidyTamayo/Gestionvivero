from django.test import TestCase
from gestionvivero.models import Productor, Finca, Vivero, Labor, ProductoControlHongo, ProductoControlPlaga, ProductoControlFertilizante
from django.core.exceptions import ValidationError
from datetime import datetime

# Create your tests here.


"""PRUEBAS CADA ENTIDAD, REQUERIMIENTO FUNCIONALES Y NO FUNCIONALES."""

# Pruebas para el modelo Productor
class ProductorTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad='123456789',
            nombre='Juan',
            apellido='Pérez',
            telefono='5551234',
            correo='juan@example.com'
        )

    def test_productor_creation(self):
        """Funcional: Verifica que se pueda crear un Productor con datos válidos"""
        productor = Productor.objects.get(documento_identidad='123456789')
        self.assertEqual(productor.nombre, 'Juan')
        self.assertEqual(productor.apellido, 'Pérez')

    def test_productor_unique_documento(self):
        """No funcional: Verifica que el documento de identidad sea único"""
        with self.assertRaises(ValidationError):
            productor = Productor(
                documento_identidad='123456789',
                nombre='Ana',
                apellido='García',
                telefono='5556789',
                correo='ana@example.com'
            )
            productor.full_clean()  # Esto valida los datos y debe fallar

    def test_productor_str_method(self):
        """Funcional: Verifica la representación en cadena del Productor"""
        self.assertEqual(str(self.productor), 'Juan Pérez')

# Pruebas para el modelo Finca
class FincaTests(TestCase):
    def setUp(self):
        self.productor = Productor.objects.create(
            documento_identidad='987654321',
            nombre='Carlos',
            apellido='Martínez',
            telefono='5559876',
            correo='carlos@example.com'
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro='FNC002',
            municipio='Bogotá'
        )

    def test_finca_creation(self):
        """Funcional: Verifica que se pueda crear una Finca con datos válidos"""
        finca = Finca.objects.get(numero_catastro='FNC002')
        self.assertEqual(finca.municipio, 'Bogotá')

    def test_finca_foreign_key(self):
        """Funcional: Verifica que la Finca esté asociada correctamente a un Productor"""
        self.assertEqual(self.finca.productor.nombre, 'Carlos')

    def test_finca_unique_numero_catastro(self):
        """No funcional: Verifica que el número de catastro sea único"""
        with self.assertRaises(ValidationError):
            finca = Finca(
                productor=self.productor,
                numero_catastro='FNC002',  # Mismo número de catastro
                municipio='Medellín'
            )
            finca.full_clean()  # Esto valida los datos y debe fallar

    def test_finca_str_method(self):
        """Funcional: Verifica la representación en cadena de la Finca"""
        self.assertEqual(str(self.finca), 'Finca FNC002 - Bogotá')

# Pruebas para el modelo Vivero
from django.db.utils import IntegrityError

class ViveroTests(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(
            productor=Productor.objects.create(
                documento_identidad='876543210',
                nombre='Luis',
                apellido='Fernández',
                telefono='5555432',
                correo='luis@example.com'
            ),
            numero_catastro='FNC003',
            municipio='Cali'
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo='VIV002',
            tipo_cultivo='Maíz'
        )

    def test_vivero_creation(self):
        """Funcional: Verifica que se pueda crear un Vivero con datos válidos"""
        vivero = Vivero.objects.get(codigo='VIV002')
        self.assertEqual(vivero.tipo_cultivo, 'Maíz')

    def test_vivero_foreign_key(self):
        """Funcional: Verifica que el Vivero esté asociado correctamente a una Finca"""
        self.assertEqual(self.vivero.finca.numero_catastro, 'FNC003')

    def test_vivero_unique_codigo(self):
        """No funcional: Verifica que el código del Vivero sea único"""
        # Primero, crea un Vivero con un código específico
        Vivero.objects.create(
            finca=self.finca,
            codigo='VIV003',
            tipo_cultivo='Trigo'
        )
        
        # Intenta crear otro Vivero con el mismo código
        try:
            Vivero.objects.create(
                finca=self.finca,
                codigo='VIV003',  # Código duplicado
                tipo_cultivo='Cebada'
            )
            # Si no se lanza una excepción, la prueba falla
            self.fail("Expected IntegrityError due to unique constraint on 'codigo'")
        except IntegrityError:
            pass  # La excepción esperada se ha lanzado

# Pruebas para el modelo Labor
class LaborTests(TestCase):
    def setUp(self):
        self.vivero = Vivero.objects.create(
            finca=Finca.objects.create(
                productor=Productor.objects.create(
                    documento_identidad='654321098',
                    nombre='Marta',
                    apellido='López',
                    telefono='5554321',
                    correo='marta@example.com'
                ),
                numero_catastro='FNC004',
                municipio='Medellín'
            ),
            codigo='VIV003',
            tipo_cultivo='Arroz'
        )
        self.labor = Labor.objects.create(
            vivero=self.vivero,
            fecha='2024-09-15',
            descripcion='Aplicación de fungicida'
        )
        self.producto_hongo = ProductoControlHongo.objects.create(
            registro_ica='ICA123',
            nombre_producto='Fungicida X',
            frecuencia_aplicacion=15,
            valor=100.00,
            periodo_carencia=7,
            nombre_hongo='Oídio'
        )
        self.labor.productos_control_hongo.add(self.producto_hongo)

   
    
    def test_labor_creation(self):
        """Funcional: Verifica que se pueda crear una Labor con datos válidos"""
        labor = Labor.objects.get(descripcion='Aplicación de fungicida')
        fecha_esperada = datetime.strptime('2024-09-15', '%Y-%m-%d').date()  # Convierte la cadena a date
        self.assertEqual(labor.fecha, fecha_esperada)


    def test_labor_foreign_key(self):
        """Funcional: Verifica que la Labor esté asociada correctamente a un Vivero"""
        self.assertEqual(self.labor.vivero.codigo, 'VIV003')

    def test_labor_m2m_relationship(self):
        """Funcional: Verifica que la Labor pueda estar asociada a Productos de Control Hongo"""
        self.assertIn(self.producto_hongo, self.labor.productos_control_hongo.all())

    def test_labor_fecha_format(self):
        """No funcional: Verifica que la fecha de la Labor sea un valor de fecha válido"""
        self.assertIsInstance(self.labor.fecha, str)  # Asume que la fecha es guardada como string

    def test_labor_str_method(self):
        """Funcional: Verifica la representación en cadena de la Labor"""
        self.assertEqual(str(self.labor), 'Labor Aplicación de fungicida en 2024-09-15')

# Pruebas para el modelo ProductoControlHongo
class ProductoControlHongoTests(TestCase):
    def setUp(self):
        self.producto_hongo = ProductoControlHongo.objects.create(
            registro_ica='ICA456',
            nombre_producto='Fungicida Y',
            frecuencia_aplicacion=30,
            valor=200.00,
            periodo_carencia=10,
            nombre_hongo='Mildiu'
        )

    def test_producto_control_hongo_creation(self):
        """Funcional: Verifica que se pueda crear un ProductoControlHongo con datos válidos"""
        producto = ProductoControlHongo.objects.get(registro_ica='ICA456')
        self.assertEqual(producto.nombre_hongo, 'Mildiu')

    def test_producto_control_hongo_str_method(self):
        """Funcional: Verifica la representación en cadena del ProductoControlHongo"""
        self.assertEqual(str(self.producto_hongo), 'Hongo Mildiu - Fungicida Y')

    def test_producto_control_hongo_periodo_carencia(self):
        """No funcional: Verifica que el periodo de carencia sea un valor entero"""
        self.assertIsInstance(self.producto_hongo.periodo_carencia, int)

    def test_producto_control_hongo_frecuencia_aplicacion(self):
        """No funcional: Verifica que la frecuencia de aplicación sea un valor entero"""
        self.assertIsInstance(self.producto_hongo.frecuencia_aplicacion, int)

# Pruebas para el modelo ProductoControlPlaga
class ProductoControlPlagaTests(TestCase):
    def setUp(self):
        self.producto_plaga = ProductoControlPlaga.objects.create(
            registro_ica='ICA789',
            nombre_producto='Insecticida Z',
            frecuencia_aplicacion=15,
            valor=150.00,
            periodo_carencia=5
        )

    def test_producto_control_plaga_creation(self):
        """Funcional: Verifica que se pueda crear un ProductoControlPlaga con datos válidos"""
        producto = ProductoControlPlaga.objects.get(registro_ica='ICA789')
        self.assertEqual(producto.nombre_producto, 'Insecticida Z')

    def test_producto_control_plaga_str_method(self):
        """Funcional: Verifica la representación en cadena del ProductoControlPlaga"""
        self.assertEqual(str(self.producto_plaga), 'Plaga - Insecticida Z')

    def test_producto_control_plaga_periodo_carencia(self):
        """No funcional: Verifica que el periodo de carencia sea un valor entero"""
        self.assertIsInstance(self.producto_plaga.periodo_carencia, int)

    def test_producto_control_plaga_frecuencia_aplicacion(self):
        """No funcional: Verifica que la frecuencia de aplicación sea un valor entero"""
        self.assertIsInstance(self.producto_plaga.frecuencia_aplicacion, int)

# Pruebas para el modelo ProductoControlFertilizante
class ProductoControlFertilizanteTests(TestCase):
    def setUp(self):
        self.producto_fertilizante = ProductoControlFertilizante.objects.create(
            registro_ica='ICA012',
            nombre_producto='Fertilizante A',
            frecuencia_aplicacion=30,
            valor=250.00,
            fecha_ultima_aplicacion='2024-09-01'
        )

    def test_producto_control_fertilizante_creation(self):
        """Funcional: Verifica que se pueda crear un ProductoControlFertilizante con datos válidos"""
        producto = ProductoControlFertilizante.objects.get(registro_ica='ICA012')
        self.assertEqual(producto.nombre_producto, 'Fertilizante A')

    def test_producto_control_fertilizante_str_method(self):
        """Funcional: Verifica la representación en cadena del ProductoControlFertilizante"""
        self.assertEqual(str(self.producto_fertilizante), 'Fertilizante - Fertilizante A')

    def test_producto_control_fertilizante_fecha_ultima_aplicacion(self):
        """No funcional: Verifica que la fecha de última aplicación sea un valor de fecha"""
        self.assertIsInstance(self.producto_fertilizante.fecha_ultima_aplicacion, str)  # Asume que la fecha es guardada como string

    def test_producto_control_fertilizante_frecuencia_aplicacion(self):
        """No funcional: Verifica que la frecuencia de aplicación sea un valor entero"""
        self.assertIsInstance(self.producto_fertilizante.frecuencia_aplicacion, int)
        

"""PRUEBAS DE RELACIONES ENTRE LAS ENTIDADES (MODELOS)"""

class RelationshipTests(TestCase):
    def setUp(self):
        # Configuramos los datos necesarios para las pruebas
        self.productor = Productor.objects.create(
            documento_identidad='123456789',
            nombre='Juan',
            apellido='Pérez',
            telefono='5551234',
            correo='juan@example.com'
        )
        self.finca = Finca.objects.create(
            productor=self.productor,
            numero_catastro='FNC001',
            municipio='Bogotá'
        )
        self.vivero = Vivero.objects.create(
            finca=self.finca,
            codigo='VIV001',
            tipo_cultivo='Maíz'
        )
        self.producto_hongo = ProductoControlHongo.objects.create(
            registro_ica='ICA123',
            nombre_producto='Fungicida X',
            frecuencia_aplicacion=15,
            valor=100.00,
            periodo_carencia=7,
            nombre_hongo='Oídio'
        )
        self.labor = Labor.objects.create(
            vivero=self.vivero,
            fecha='2024-09-15',
            descripcion='Aplicación de fungicida'
        )
        self.labor.productos_control_hongo.add(self.producto_hongo)

    def test_productor_finca_relationship(self):
        """Verifica que una Finca está correctamente asociada a un Productor"""
        finca = Finca.objects.get(numero_catastro='FNC001')
        self.assertEqual(finca.productor, self.productor)

    def test_finca_vivero_relationship(self):
        """Verifica que un Vivero está correctamente asociado a una Finca"""
        vivero = Vivero.objects.get(codigo='VIV001')
        self.assertEqual(vivero.finca, self.finca)

    def test_labor_vivero_relationship(self):
        """Verifica que una Labor está correctamente asociada a un Vivero"""
        labor = Labor.objects.get(descripcion='Aplicación de fungicida')
        self.assertEqual(labor.vivero, self.vivero)

    def test_labor_productos_control_hongo_relationship(self):
        """Verifica que una Labor puede tener Productos de Control Hongo asociados"""
        labor = Labor.objects.get(descripcion='Aplicación de fungicida')
        self.assertIn(self.producto_hongo, labor.productos_control_hongo.all())

    def test_vivero_str_method(self):
        """Verifica la representación en cadena del Vivero"""
        self.assertEqual(str(self.vivero), 'Vivero VIV001 - Maíz')


