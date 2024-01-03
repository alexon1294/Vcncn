from .entities.Comprobante import Comprobante

class ModelComprobante:

    @classmethod
    def crear_comrpobante(cls, db, id_cliente, id_lote, id_aplicante, fecha_emision):
        try:
            insert_query = """
            INSERT INTO comprobantes (NOMBRE_CLIENTE, A_PATERNO_CLIENTE, A_MATERNO_CLIENTE, NOMBRE_COMPLETO_APLICANTE, LOTE, FECHA_EMISION, ID_CLIENTE, ID_LOTE, ID_APLICANTE)
            SELECT registros.NOMBRE, registros.A_PATERNO, registros.A_MATERNO, aplicantes.NOMBRE_COMPLETO_APLICANTE, lotes.NUMERO_LOTE, %s, %s, %s, %s
            FROM (
                SELECT NOMBRE, A_PATERNO, A_MATERNO
                FROM registros
                WHERE ID = %s
            ) registros
            JOIN (
                SELECT NOMBRE_COMPLETO_APLICANTE
                FROM aplicantes
                WHERE ID_APLICANTE = %s
            ) aplicantes
            JOIN (
                SELECT NUMERO_LOTE
                FROM lotes
                WHERE ID_LOTE = %s
            ) lotes
            """
            with db.connection.cursor() as cursor:
                cursor.execute(insert_query, (fecha_emision, id_cliente, id_lote, id_aplicante, id_cliente, id_aplicante, id_lote))
                db.connection.commit()

                # Actualizamos la columna COMPROBANTE a 1 en la tabla registros para tener el mensaje "Volver a imprimir" y ademas los tres campos que estaban en "Pendiente"
                update_query = """
                UPDATE registros
                SET COMPROBANTE = 1,
                    FECHA_EMISION_COMPROBANTE = %s,
                    NOMBRE_APLICANTE = (
                        SELECT NOMBRE_COMPLETO_APLICANTE
                        FROM aplicantes
                        WHERE ID_APLICANTE = %s
                    ),
                    LOTE = (
                        SELECT NUMERO_LOTE
                        FROM lotes
                        WHERE ID_LOTE = %s
                    )
                WHERE ID = %s
                """
                cursor.execute(update_query, (fecha_emision, id_aplicante, id_lote, id_cliente))
                db.connection.commit()

            return True
        except Exception as e:
            print(f"Error al crear el comprobante: {e}")
            return False