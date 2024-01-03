from .entities.Aplicante import Aplicante


class ModelAplicante:

    @classmethod
    def get_aplicante_rows(cls, db):
        try:
            aplicante_rows = []

            with db.connection.cursor() as cursor:
                cursor.execute("SELECT ID_APLICANTE, NOMBRE_COMPLETO_APLICANTE FROM aplicantes")
                resultset = cursor.fetchall()
                for row in resultset:
                    aplicante = Aplicante(row[0], row[1])
                    aplicante_rows.append(aplicante.to_dict())

            return aplicante_rows
        except Exception as ex:
            print(f"Error al obtener filas de aplicantes: {ex}")
            return []
    
    @classmethod
    def guardar_nuevo_aplicante(cls, db, aplicante):
        try:
            # Verificamos si el aplicante ya existe en la tabla de aplicantes
            select_query = "SELECT COUNT(*) FROM aplicantes WHERE NOMBRE_COMPLETO_APLICANTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(select_query, (aplicante,))
                result = cursor.fetchone()
                if result[0] > 0: 
                    print('El aplicante ya existe en la tabla de aplicantes.')
                    return None

            # Si el aplicante no existe, lo insertamos en la base de datos
            insert_query = "INSERT INTO aplicantes (NOMBRE_COMPLETO_APLICANTE) VALUES (%s)"
            select_last_id_query = "SELECT LAST_INSERT_ID()"

            with db.connection.cursor() as cursor:
                cursor.execute(insert_query, (aplicante,))
                db.connection.commit()
                cursor.execute(select_last_id_query)
                last_id_aplicante = cursor.fetchone()[0]

            return last_id_aplicante
        except Exception as e:
            print("Error al guardar el nuevo aplicante:", str(e))
            return None

    @classmethod
    def borrar_aplicante(cls, db, id_aplicante):
        try:
            # Verificamos si el lote existe en la tabla de lotes
            select_query = "SELECT COUNT(*) FROM aplicantes WHERE ID_APLICANTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(select_query, (id_aplicante,))
                result = cursor.fetchone()
                if result[0] == 0: 
                    return False

            # Si el lote existe, lo borramos
            delete_query = "DELETE FROM aplicantes WHERE ID_APLICANTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(delete_query, (id_aplicante,))
                db.connection.commit()
            return True
        except Exception as e:
            print("Error al eliminar Aplicante, puede que ya exista un comprobante asociado al aplicante:", str(e))
            return False