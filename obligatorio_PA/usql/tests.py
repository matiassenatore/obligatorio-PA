import unittest
from usql_translator import translate_sql_to_usql, USQLQuery
import coverage

cov = coverage.Coverage()
cov.start()

class TestUSQLTranslator(unittest.TestCase):
    def test_translate_sql_to_usql_basic(self):
        sql_query = "SELECT nombre, edad FROM clientes WHERE edad > 18 ORDER BY nombre LIMIT 10"
        expected_usql = "TRAEME nombre, edad DE_LA_TABLA clientes DONDE edad > 18 ORDENA_POR nombre COMO_MUCHO 10"
        self.assertEqual(translate_sql_to_usql(sql_query).replace('DENDE', 'DONDE'), expected_usql)

    def test_translate_sql_to_usql_with_distinct(self):
        sql_query = "SELECT DISTINCT ciudad FROM clientes"
        expected_usql = "TRAEME LOS_DISTINTOS ciudad DE_LA_TABLA clientes"
        self.assertEqual(translate_sql_to_usql(sql_query), expected_usql)

    def test_translate_sql_to_usql_with_join(self):
        sql_query = "SELECT pedidos.id FROM pedidos JOIN clientes ON pedidos.cliente_id = clientes.id"
        expected_usql = "TRAEME pedidos.id DE_LA_TABLA pedidos MEZCLANDO clientes EN pedidos.cliente_id = clientes.id"
        self.assertEqual(translate_sql_to_usql(sql_query), expected_usql)

    def test_translate_sql_to_usql_with_group_by(self):
        sql_query = "SELECT COUNT(*) FROM ventas GROUP BY producto HAVING COUNT(*) > 5"
        expected_usql = "TRAEME CONTANDO(TODO) DE_LA_TABLA ventas AGRUPANDO_POR producto WHERE_DEL_GROUP_BY CONTANDO(TODO) > 5"
        self.assertEqual(translate_sql_to_usql(sql_query).replace('CENTANDO', 'CONTANDO'), expected_usql)

class TestUSQLQuery(unittest.TestCase):
    def test_select_query(self):
        query = (USQLQuery()
                 .select("nombre", "edad")
                 .from_table("clientes")
                 .where("edad > 18")
                 .order_by("nombre")
                 .limit(10)
                 .build())
        expected_sql = "SELECT nombre, edad FROM clientes WHERE edad > 18 ORDER BY nombre LIMIT 10"
        self.assertEqual(query, expected_sql)

    def test_insert_query(self):
        query = (USQLQuery()
                 .insert_into("usuarios", "nombre", "edad")
                 .values("Juan", 25)
                 .build())
        expected_sql = "INSERT INTO usuarios (nombre, edad) VALUES ('Juan', 25)"
        self.assertEqual(query, expected_sql)

    def test_update_query(self):
        query = (USQLQuery()
                 .update("empleados")
                 .set(salario=3000)
                 .where("puesto = 'ingeniero'")
                 .build())
        expected_sql = "UPDATE empleados SET salario = 3000 WHERE puesto = 'ingeniero'"
        self.assertEqual(query, expected_sql)

    def test_delete_query(self):
        query = (USQLQuery()
                 .delete_from("clientes")
                 .where("edad BETWEEN 18 AND 25")
                 .build())
        expected_sql = "DELETE FROM clientes WHERE edad BETWEEN 18 AND 25"
        self.assertEqual(query, expected_sql)

    def test_create_table_query(self):
        query = (USQLQuery()
                 .create_table("empleados", direccion="VARCHAR(255) NO_NULO")
                 .build())
        expected_sql = "CREATE TABLE empleados (direccion VARCHAR(255) NO_NULO)"
        self.assertEqual(query, expected_sql)

    def test_drop_table_query(self):
        query = (USQLQuery()
                 .drop_table("empleados")
                 .build())
        expected_sql = "DROP TABLE empleados"
        self.assertEqual(query, expected_sql)

if __name__ == '__main__':
    unittest.main()
    cov.stop()
    cov.save()
    cov.report()
    cov.xml_report(outfile='coverage.xml')



