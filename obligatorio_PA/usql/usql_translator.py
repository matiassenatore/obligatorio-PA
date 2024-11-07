import ply.lex as lex
import ply.yacc as yacc
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

usql_keywords = {
    'TRAEME': 'SELECT',
    'TODO': '*',
    'DE_LA_TABLA': 'FROM',
    'DONDE': 'WHERE',
    'AGRUPANDO_POR': 'GROUP BY',
    'LOS_DISTINTOS': 'DISTINCT',
    'CONTANDO': 'COUNT',
    'METE_EN': 'INSERT INTO',
    'LOS_VALORES': 'VALUES',
    'ACTUALIZA': 'UPDATE',
    'SETEA': 'SET',
    'BORRA_DE_LA': 'DELETE FROM',
    'ORDENA_POR': 'ORDER BY',
    'COMO_MUCHO': 'LIMIT',
    'WHERE_DEL_GROUP_BY': 'HAVING',
    'CAMBIA_LA_TABLA': 'ALTER TABLE',
    'AGREGA_LA_COLUMNA': 'ADD COLUMN',
    'ELIMINA_LA_COLUMNA': 'DROP COLUMN',
    'NO_NULO': 'NOT NULL',
    'MEZCLANDO': 'JOIN',
    'EN': 'ON',
    'EXISTE': 'EXISTS',
    'ENTRE': 'BETWEEN',
    'PARECIDO_A': 'LIKE',
    'ES_NULO': 'IS NULL',
    'CREA_LA_TABLA': 'CREATE TABLE',
    'TIRA_LA_TABLA': 'DROP TABLE',
    'POR_DEFECTO': 'DEFAULT',
    'UNICO': 'UNIQUE',
    'CLAVE_PRIMA': 'PRIMARY KEY',
    'CLAVE_REFERENTE': 'FOREIGN KEY'
}

tokens = list(usql_keywords.keys()) + [
    'ID', 'NUMERO', 'CADENA', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'COMA', 'Y'
]

t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_COMA = r','
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMERO = r'\d+'
t_CADENA = r"'[^']*'"
t_Y = r'Y'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in usql_keywords:
        t.type = t.value  
    else:
        t.type = 'ID'  
    return t

def t_error(t):
    logging.error(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_query(t):
    '''query : select_statement
             | insert_statement
             | update_statement
             | delete_statement
             | alter_statement
             | create_table_statement
             | drop_table_statement'''
    t[0] = t[1]

def p_select_statement(t):
    '''select_statement : TRAEME select_list DE_LA_TABLA ID join_clause optional_clauses'''
    t[0] = f"SELECT {t[2]} FROM {t[4]} {t[5]} {t[6]}"

def p_select_list(t):
    '''select_list : TODO
                   | LOS_DISTINTOS ID
                   | CONTANDO PARENTESIS_IZQ TODO PARENTESIS_DER'''
    if len(t) == 2:
        t[0] = '*'
    elif t[1] == 'LOS_DISTINTOS':
        t[0] = f"DISTINCT {t[2]}"
    else:
        t[0] = "COUNT(*)"

def p_join_clause(t):
    '''join_clause : MEZCLANDO ID EN condition
                   | empty'''
    t[0] = f"JOIN {t[2]} ON {t[4]}" if len(t) > 2 else ""

def p_optional_clauses(t):
    '''optional_clauses : where_clause group_by_clause having_clause order_by_clause limit_clause'''
    t[0] = f"{t[1]} {t[2]} {t[3]} {t[4]} {t[5]}"

def p_where_clause(t):
    '''where_clause : DONDE condition
                    | empty'''
    t[0] = f"WHERE {t[2]}" if len(t) > 2 else ""

def p_group_by_clause(t):
    '''group_by_clause : AGRUPANDO_POR ID
                       | empty'''
    t[0] = f"GROUP BY {t[2]}" if len(t) > 2 else ""

def p_having_clause(t):
    '''having_clause : WHERE_DEL_GROUP_BY condition
                     | empty'''
    t[0] = f"HAVING {t[2]}" if len(t) > 2 else ""

def p_order_by_clause(t):
    '''order_by_clause : ORDENA_POR ID
                       | empty'''
    t[0] = f"ORDER BY {t[2]}" if len(t) > 2 else ""

def p_limit_clause(t):
    '''limit_clause : COMO_MUCHO NUMERO
                    | empty'''
    t[0] = f"LIMIT {t[2]}" if len(t) > 2 else ""

def p_condition(t):
    '''condition : ID '=' value
                 | ID '>' value
                 | ID '<' value
                 | ID ENTRE value Y value
                 | ID PARECIDO_A CADENA
                 | ID ES_NULO'''
    if len(t) == 4:
        t[0] = f"{t[1]} {t[2]} {t[3]}"
    elif t[2] == 'ENTRE':
        t[0] = f"{t[1]} BETWEEN {t[3]} AND {t[5]}"
    elif t[2] == 'PARECIDO_A':
        t[0] = f"{t[1]} LIKE {t[3]}"
    elif t[2] == 'ES_NULO':
        t[0] = f"{t[1]} IS NULL"

def p_insert_statement(t):
    '''insert_statement : METE_EN ID PARENTESIS_IZQ column_list PARENTESIS_DER LOS_VALORES PARENTESIS_IZQ value_list PARENTESIS_DER'''
    t[0] = f"INSERT INTO {t[2]} ({t[4]}) VALUES ({t[8]})"

def p_column_list(t):
    '''column_list : ID
                   | column_list COMA ID'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

def p_value_list(t):
    '''value_list : value
                  | value_list COMA value'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

def p_update_statement(t):
    '''update_statement : ACTUALIZA ID SETEA ID '=' value where_clause'''
    t[0] = f"UPDATE {t[2]} SET {t[4]} = {t[6]} {t[7]}"

def p_value(t):
    '''value : CADENA
             | NUMERO'''
    t[0] = t[1]

def p_delete_statement(t):
    '''delete_statement : BORRA_DE_LA ID where_clause'''
    t[0] = f"DELETE FROM {t[2]} {t[3]}"

def p_alter_statement(t):
    '''alter_statement : CAMBIA_LA_TABLA ID alter_action'''
    t[0] = f"ALTER TABLE {t[2]} {t[3]}"

def p_alter_action(t):
    '''alter_action : AGREGA_LA_COLUMNA ID type not_null
                    | ELIMINA_LA_COLUMNA ID'''
    if len(t) == 5:
        t[0] = f"ADD COLUMN {t[2]} {t[3]} {t[4]}"
    else:
        t[0] = f"DROP COLUMN {t[2]}"

def p_type(t):
    '''type : ID'''
    t[0] = t[1]

def p_not_null(t):
    '''not_null : NO_NULO
                | empty'''
    t[0] = t[1] if len(t) > 1 else ''

def p_create_table_statement(t):
    '''create_table_statement : CREA_LA_TABLA ID PARENTESIS_IZQ column_definitions PARENTESIS_DER'''
    t[0] = f"CREATE TABLE {t[2]} ({t[4]})"

def p_column_definitions(t):
    '''column_definitions : column_definition
                          | column_definitions COMA column_definition'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}, {t[3]}"

def p_column_definition(t):
    '''column_definition : ID type column_constraints'''
    t[0] = f"{t[1]} {t[2]} {t[3]}"

def p_column_constraints(t):
    '''column_constraints : not_null
                          | UNICO
                          | CLAVE_PRIMA
                          | CLAVE_REFERENTE PARENTESIS_IZQ ID PARENTESIS_DER
                          | empty'''
    if len(t) == 2:
        t[0] = t[1]
    elif t[1] == 'CLAVE_REFERENTE':
        t[0] = f"FOREIGN KEY ({t[3]})"
    else:
        t[0] = ''

def p_drop_table_statement(t):
    '''drop_table_statement : TIRA_LA_TABLA ID'''
    t[0] = f"DROP TABLE {t[2]}"

def p_empty(t):
    '''empty :'''
    t[0] = ''

def p_error(t):
    if t:
        logging.error(f"Error de sintaxis en '{t.value}', línea {t.lineno}")
        raise SyntaxError(f"Error de sintaxis en '{t.value}'")
    else:
        logging.error("Error de sintaxis en el final del archivo")
        raise SyntaxError("Error de sintaxis en el final del archivo")

parser = yacc.yacc()

def translate_sql_to_usql(sql_query):
    translations = {
        'SELECT': 'TRAEME',
        '*': 'TODO',
        'FROM': 'DE_LA_TABLA',
        'WHERE': 'DONDE',
        'GROUP BY': 'AGRUPANDO_POR',
        'DISTINCT': 'LOS_DISTINTOS',
        'COUNT': 'CONTANDO',
        'INSERT INTO': 'METE_EN',
        'VALUES': 'LOS_VALORES',
        'UPDATE': 'ACTUALIZA',
        'SET': 'SETEA',
        'DELETE FROM': 'BORRA_DE_LA',
        'ORDER BY': 'ORDENA_POR',
        'LIMIT': 'COMO_MUCHO',
        'HAVING': 'WHERE_DEL_GROUP_BY',
        'ALTER TABLE': 'CAMBIA_LA_TABLA',
        'ADD COLUMN': 'AGREGA_LA_COLUMNA',
        'DROP COLUMN': 'ELIMINA_LA_COLUMNA',
        'NOT NULL': 'NO_NULO',
        'JOIN': 'MEZCLANDO',
        'ON': 'EN',
        'EXISTS': 'EXISTE',
        'BETWEEN': 'ENTRE',
        'LIKE': 'PARECIDO_A',
        'IS NULL': 'ES_NULO',
        'CREATE TABLE': 'CREA_LA_TABLA',
        'DROP TABLE': 'TIRA_LA_TABLA',
        'DEFAULT': 'POR_DEFECTO',
        'UNIQUE': 'UNICO',
        'PRIMARY KEY': 'CLAVE_PRIMA',
        'FOREIGN KEY': 'CLAVE_REFERENTE'
    }
    
    usql_query = sql_query
    for sql_keyword, usql_keyword in translations.items():
        usql_query = usql_query.replace(sql_keyword, usql_keyword)
    
    return usql_query

class USQLQuery:
    def __init__(self):
        self.query_parts = []

    def select(self, *columns):
        columns_str = ', '.join(columns) if columns else '*'
        self.query_parts.append(f"SELECT {columns_str}")
        return self

    def from_table(self, table_name):
        self.query_parts.append(f"FROM {table_name}")
        return self

    def where(self, condition):
        self.query_parts.append(f"WHERE {condition}")
        return self

    def group_by(self, *columns):
        columns_str = ', '.join(columns)
        self.query_parts.append(f"GROUP BY {columns_str}")
        return self

    def having(self, condition):
        self.query_parts.append(f"HAVING {condition}")
        return self

    def order_by(self, *columns):
        columns_str = ', '.join(columns)
        self.query_parts.append(f"ORDER BY {columns_str}")
        return self

    def limit(self, number):
        self.query_parts.append(f"LIMIT {number}")
        return self

    def join(self, table_name, condition):
        self.query_parts.append(f"JOIN {table_name} ON {condition}")
        return self

    def insert_into(self, table_name, *columns):
        columns_str = ', '.join(columns)
        self.query_parts.append(f"INSERT INTO {table_name} ({columns_str})")
        return self

    def values(self, *values):
        values_str = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in values])
        self.query_parts.append(f"VALUES ({values_str})")
        return self

    def update(self, table_name):
        self.query_parts.append(f"UPDATE {table_name}")
        return self

    def set(self, **kwargs):
        set_str = ', '.join([f"{column} = '{value}'" if isinstance(value, str) else f"{column} = {value}" for column, value in kwargs.items()])
        self.query_parts.append(f"SET {set_str}")
        return self

    def delete_from(self, table_name):
        self.query_parts.append(f"DELETE FROM {table_name}")
        return self

    def create_table(self, table_name, **columns):
        columns_str = ', '.join([f"{name} {definition}" for name, definition in columns.items()])
        self.query_parts.append(f"CREATE TABLE {table_name} ({columns_str})")
        return self

    def drop_table(self, table_name):
        self.query_parts.append(f"DROP TABLE {table_name}")
        return self

    def build(self):
        try:
            query = ' '.join(self.query_parts)
            if not query:
                raise ValueError("La consulta no puede estar vacía")
            return query
        except Exception as e:
            logging.error(f"Error al construir la consulta: {e}")
            raise





