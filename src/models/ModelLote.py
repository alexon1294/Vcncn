from .entities.Lote import Lote


class ModelLote:

    @classmethod
    def get_lote_rows(cls, db):
        try:
            lote_rows = []

            with db.connection.cursor() as cursor:
                cursor.execute("SELECT ID_LOTE, NUMERO_LOTE FROM lotes")
                resultset = cursor.fetchall()
                for row in resultset:
                    lote = Lote(row[0], row[1])
                    lote_rows.append(lote.to_dict())

            return lote_rows
        except Exception as ex:
            print(f"Error al obtener filas de lotes: {ex}")
            return []

    @classmethod
    def guardar_nuevo_lote(cls, db, lote):
        try:
            # Verificamos si el lote ya existe en la tabla de lotes
            select_query = "SELECT COUNT(*) FROM lotes WHERE NUMERO_LOTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(select_query, (lote,))
                result = cursor.fetchone()
                if result[0] > 0:  # Accede al primer elemento de la tupla result
                    print('El lote ya existe en la tabla lotes.')
                    return None

            # Si el lote no existe, se procede a insertarlo
            insert_query = "INSERT INTO lotes (NUMERO_LOTE) VALUES (%s)"
            select_last_id_query = "SELECT LAST_INSERT_ID()"

            with db.connection.cursor() as cursor:
                cursor.execute(insert_query, (lote,))
                db.connection.commit()
                cursor.execute(select_last_id_query)
                last_id = cursor.fetchone()[0]

            print(f'Nuevo lote guardado en la tabla lotes. id : {last_id}')
            return last_id
        except Exception as e:
            print("Error al guardar el nuevo lote:", str(e))
            return None

    @classmethod
    def borrar_lote(cls, db, id_lote):
        try:
            # Verificamos si el lote existe en la tabla de lotes
            select_query = "SELECT COUNT(*) FROM lotes WHERE ID_LOTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(select_query, (id_lote,))
                result = cursor.fetchone()
                if result[0] == 0:
                    return False

            # Si el lote existe, lo borramos
            delete_query = "DELETE FROM lotes WHERE ID_LOTE = %s"

            with db.connection.cursor() as cursor:
                cursor.execute(delete_query, (id_lote,))
                db.connection.commit()
            return True
        except Exception as e:
            print("Error al eliminar el lote:", str(e))
            return False
