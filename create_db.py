import pandas as pd
import sqlite3

# Leer el archivo de Excel con la hoja de artículos
file_path = '\FULL DATABASE READY TO USE.xlsx'
articles_data = pd.read_excel(file_path, sheet_name='articulos')  # Ajustar 'Sheet1' al nombre de la hoja de artículos

# Conectar a la base de datos SQLite (se creará si no existe)
conn = sqlite3.connect('articulos.db')
cursor = conn.cursor()

# Definir la estructura de las tablas (clave primaria y foránea)
table_definitions = {
    'articles': {
        'columns': {
            'OWN_ID': 'INTEGER PRIMARY KEY',
            'Title': 'TEXT',
            'YEAR': 'INTEGER',
            'Source_title': 'TEXT',
            'Number_of_appointments': 'INTEGER',
            'Abstract': 'TEXT',
            'Author_Keywords': 'TEXT',
            'Code_Keyword': 'INTEGER',
            'Code_JCR_RANK': 'INTEGER',
            'AREA_OF_KNOWLEDGE': 'TEXT',
            'Code_Area_of_Knowledge': 'INTEGER'
        },
        'foreign_keys': [
            ('Number_of_appointments', 'appointment(Code)'),
            ('YEAR', 'years(Code)'),
            ('Code_Keyword', 'keyword(Code)'),
            ('Code_JCR_RANK', 'JCR_rank(Code)'),
            ('Code_Area_of_Knowledge', 'area_of_knowledge(Code)')
        ]
    },
    'appointment': {
        'columns': {
            'Appointment': 'TEXT',
            'Code': 'INTEGER PRIMARY KEY'
        },
        'data': [
            ('No appointment', 0),
            ('1-10', 1),
            ('11-24', 2),
            ('25-49', 3),
            ('50-99', 4),
            ('100-249', 5),
            ('De 250 or more', 6),
            ('N/C', 99)
        ]
    },
    'years': {
        'columns': {
            'Year': 'TEXT',
            'Code': 'INTEGER PRIMARY KEY'
        },
        'data': [
            ('1996-2008', 1),
            ('2009-2019', 2),
            ('2020-2024', 3)
        ]
    },
    'area_of_knowledge': {
        'columns': {
            'Code_Area_of_Knowledge': 'TEXT',
            'Code': 'INTEGER PRIMARY KEY'
        },
        'data': [
            ('No code', 0),
            ('Humanities', 1),
            ('Other social sciences', 2),
            ('Science', 3),
            ('Economics and business', 4)
        ]
    },
    'keyword': {
        'columns': {
            'Keyword': 'TEXT',
            'Code': 'INTEGER PRIMARY KEY'
        },
        'data': [
            ('Advertising', 1),
            ('Augmented reality', 2),
            ('Authenticity', 3),
            ('Avatars', 4),
            ('Blockchain', 5),
            ('Brand equity', 6),
            ('Branding', 7),
            ('Brands', 8),
            ('Extended reality', 9),
            ('Immersive', 10),
            ('Marketing', 11),
            ('Metaverse', 12),
            ('Second life', 13),
            ('Social medial', 14),
            ('Video Game', 15),
            ('Virtual reality', 16),
            ('Virtual Worlds', 17),
            ('Artificial intelligence', 18)
        ]
    },
    'JCR_rank': {
        'columns': {
            'JCR_RANK': 'TEXT',
            'Code': 'INTEGER PRIMARY KEY'
        },
        'data': [
            ('N/C', 0),
            ('Q1', 1),
            ('Q2', 2),
            ('Q3', 3),
            ('Q4', 4)
        ]
    }
}

# Crear las tablas en la base de datos
for table_name, table_info in table_definitions.items():
    columns = table_info['columns']
    columns_str = ', '.join([f'"{col}" {dtype}' for col, dtype in columns.items()])
    
    # Añadir claves foráneas si existen
    if 'foreign_keys' in table_info:
        foreign_keys_str = ', '.join([f'FOREIGN KEY({fk[0]}) REFERENCES {fk[1]}' for fk in table_info['foreign_keys']])
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_str}, {foreign_keys_str})'
    else:
        create_table_query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_str})'
    
    cursor.execute(create_table_query)

    # Insertar datos directos si existen
    if 'data' in table_info:
        insert_query = f'INSERT INTO "{table_name}" ({", ".join(columns.keys())}) VALUES ({", ".join(["?"] * len(columns))})'
        cursor.executemany(insert_query, table_info['data'])

# Insertar los datos en la tabla de artículos
columns = table_definitions['articles']['columns']
for index, row in articles_data.iterrows():
    placeholders = ', '.join(['?'] * len(row))
    insert_query = f'INSERT INTO "articles" ({", ".join(columns.keys())}) VALUES ({placeholders})'
    cursor.execute(insert_query, tuple(row))

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada y datos insertados con éxito.")
