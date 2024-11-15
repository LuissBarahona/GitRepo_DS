import pymysql

class DAOCursos:
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password="", db="db_poo")

    def read(self):
        try:
            with self.connect() as con:
                with con.cursor() as cursor:
                    cursor.execute("SELECT * FROM cursos")
                    result = cursor.fetchall()  # Recupera todos los cursos
                    cursos = []
                    for row in result:
                        cursos.append({
                            'idCurso': row[0],
                            'nombreCurso': row[1],
                            'descripcion': row[2],
                            'categoria': row[3],
                            'fechaCreacion': row[4],
                            'imagen': row[5],
                            'precio': row[6]
                        })
                    return cursos
        except pymysql.MySQLError as e:
            print(f"Error en la consulta: {e}")
            return []