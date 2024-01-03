from .entities.Table import Table
import pandas as pd
import math


class ModelTable:

    @classmethod
    def get_table_rows(cls, db, search=None, columns=None):
        try:
            cursor = db.connection.cursor()

            # Definimos las columnas que se seleccionarán en la consulta SQL
            if columns:
                selected_columns = ', '.join(columns)
            else:
                selected_columns = "*"

            sql = f"SELECT {selected_columns} FROM registros"

            # Si hay un término de búsqueda, lo añádimos a la consulta SQL
            if search:
                search_conditions = " OR ".join([f"{column} LIKE %s" for column in columns])
                sql += f" WHERE {search_conditions}"
                search_param = f"%{search}%"
                cursor.execute(sql, tuple([search_param] * len(columns)))
            else:
                cursor.execute(sql)

            Table_rows = []
            with cursor:
                resultset = cursor.fetchall()
                for row in resultset:
                    imprimir_string = 'Volver a imprimir' if row[15] == 1 else 'Imprimir'
                    row = Table(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], imprimir_string, row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26])
                    Table_rows.append(row.to_dict())
            cursor.close()
            return Table_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_data_from_excel(cls, file_path, num_rows=None):
        try:
            df = pd.read_excel(file_path, nrows=num_rows)
            data = df.to_dict('records')
            return data
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            return []
        
    @classmethod
    def validate_data_format(cls,data_from_excel, db):
        # Obtenemos información de la estructura de la tabla desde la base de datos
        with db.connection.cursor() as cursor:
            cursor.execute("DESCRIBE registros")
            table_columns = [column[0] for column in cursor.fetchall()]

        # Verificamos si las columnas del Excel coinciden con las de la tabla en la base de datos
        excel_columns = data_from_excel[0].keys()  # La primera fila debe tener los encabezados
        if set(excel_columns) != set(table_columns):
            raise ValueError("Las columnas del archivo Excel no coinciden con la estructura de la tabla en la base de datos")
        
    @classmethod
    def update_table_from_excel(cls, db, file_path):
        try:
            # Cargamos y validamos las columnas de los datos desde el archivo Excel
            data_from_excel = cls.get_data_from_excel(file_path)
            # cls.validate_data_format(data_from_excel, db)
            cleaned_data = []
            for row in data_from_excel:
                cleaned_row = {key: ('Ninguna' if (isinstance(value, float) and math.isnan(value)) else value) for key, value in row.items()}

                if 'FECHA_HORA_REGISTRO' in cleaned_row and 'F_NACIMIENTO' in cleaned_row:
                    fecha_hora = cleaned_row['FECHA_HORA_REGISTRO']
                    fecha_nacimiento = row['F_NACIMIENTO']

                    # Convertimos a formato datetime
                    fecha_hora = pd.to_datetime(fecha_hora, format='%d/%m/%Y %I:%M:%S %p')
                    fecha_nacimiento = pd.to_datetime(fecha_nacimiento, format='%d/%m/%Y')
                    
                    # Extraemos fecha y hora sin segundos y formateamos fecha de nacimiento
                    fecha_hora_sin_segundos = fecha_hora.strftime('%d/%m/%Y %I:%M %p')
                    fecha_nacimiento_formateada = fecha_nacimiento.strftime('%d/%m/%Y')

                    # Actualizamos el valor en 'cleaned_row' con el formato de hora y minutos
                    cleaned_row['FECHA_HORA_REGISTRO'] = fecha_hora_sin_segundos
                    cleaned_row['F_NACIMIENTO'] = fecha_nacimiento_formateada

                    cleaned_data.append(cleaned_row)
            # Eliminamos los datos existentes de la tabla
            with db.connection.cursor() as cursor:
                delete_sql = "DELETE FROM registros"
                cursor.execute(delete_sql)

            # Reiniciamos el ID
            with db.connection.cursor() as cursor:
                reset_auto_increment = "ALTER TABLE registros AUTO_INCREMENT = 1"
                cursor.execute(reset_auto_increment)

            # Insertamos los nuevos datos    
            with db.connection.cursor() as cursor:
                for row in cleaned_data:
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(row.keys())
                    values = tuple(row.values())
                    insert_sql = f"INSERT INTO registros ({columns}) VALUES ({placeholders})"
                    cursor.execute(insert_sql, values)
                db.connection.commit()
            
            return print("Actualización exitosa")
            
        except Exception as ex:
            raise ex
        
    @classmethod
    def update_table_row(cls, db, row):
        try:
            # 'ID' es el identificador de la fila a actualizar
                                        
            update_query = """UPDATE registros
                        SET NOMBRE = %s, A_PATERNO = %s, A_MATERNO = %s,
                        F_NACIMIENTO = %s, EDAD = %s, SEXO = %s,
                        ALERGIAS = %s, ALERGIA_ESPECIFICA = %s, FECHA_ULTIMA_VAC_COVID = %s,
                        FECHA_ULTIMA_VAC_INFLUENZA = %s, TELEFONO = %s, EMAIL = %s,
                        CALLE = %s, NUM_EXT = %s, COLONIA = %s,
                        ALCALDIA = %s, CP = %s WHERE ID = %s"""
            # Seleccionamos los valores para la consulta
            new_query_row_values = (
                row[1], row[2], row[3], row[4], row[5], row[6], 
                row[7], row[8], row[9], row[10], row[13], row[14], row[15], 
                row[16], row[17], row[18], row[19], int(row[0])
            )
            print(new_query_row_values)
            with db.connection.cursor() as cursor:
                cursor.execute(update_query, new_query_row_values)
                db.connection.commit()
            return True
        except Exception as e:
            # db.rollback()  # Revertir cambios en caso de error
            print("Tipo de error:", type(e).__name__)
            print("Error en la actualización:", str(e))
            return False

    @classmethod
    def actualizar_tabla_comprobante(cls, db, id_registro, fecha_emision, nombre_aplicante, lote):
        try:
            update_query = """
                UPDATE registros 
                SET FECHA_EMISION_COMPROBANTE = %s, NOMBRE_APLICANTE = %s, LOTE = %s
                WHERE ID = %s
            """
            
            new_query_row_values = (fecha_emision, nombre_aplicante, lote, id_registro)

            with db.connection.cursor() as cursor:
                cursor.execute(update_query, new_query_row_values)
                db.connection.commit()
            return True
        except Exception as e:
            # db.rollback()  # Revertir cambios en caso de error
            print("Error en la actualización:", str(e))
            return False

    @classmethod
    def add_new_row(cls, db, datos):
        try:
            insert_query = """INSERT INTO registros 
                            (FECHA_HORA_REGISTRO, NOMBRE, A_PATERNO, A_MATERNO, F_NACIMIENTO, EDAD, SEXO,
                            ALERGIAS, ALERGIA_ESPECIFICA, FECHA_ULTIMA_VAC_COVID,
                            FECHA_ULTIMA_VAC_INFLUENZA, TELEFONO, EMAIL, CALLE,
                            NUM_EXT, COLONIA, ALCALDIA, CP, VACUNA_SARS_COV2, VACUNA_INFLUENZA_VAXIGRIP)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            values = (
                datos[0], datos[1], datos[2], datos[3], datos[4], datos[5],
                datos[6], datos[7], datos[8], datos[9], datos[10], datos[11],
                datos[12], datos[13], datos[14], datos[15], datos[16], datos[17], datos[18], datos[19]
            )

            with db.connection.cursor() as cursor:
                cursor.execute(insert_query, values)
                db.connection.commit()
            return True
        except Exception as e:
            print("Tipo de error:", type(e).__name__)
            print("Error al agregar fila:", str(e))
            return False
    

