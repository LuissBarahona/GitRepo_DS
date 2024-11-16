import pymysql

class DAOEstudiante:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_poo" )
        #cambiara localhost -> db y poner a password=root cuando se suba a la nube
        
    def read(self, username):
            try:
                with self.connect() as con:
                    with con.cursor() as cursor:
                        cursor.execute("SELECT * FROM registroEstudiante WHERE correo = %s OR nombreUsuario = %s", (username, username))
                        result = cursor.fetchone()
                        if result:
                            # Devuelve un diccionario con los datos del usuario
                            return {
                                'id': result[0],
                                'nombre': result[1],
                                'apellido': result[2],
                                'nombreUsuario': result[3],
                                'correo': result[4],
                                'contrasena': result[5]
                            }
                        return None
            except pymysql.MySQLError as e:
                print(f"Error en la consulta: {e}")
                return None

    def insert(self,data):
        con = DAOEstudiante.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO registroEstudiante(nombre,apellido,nombreUsuario,correo,contrasena) VALUES(%s, %s, %s, %s, %s)", (data['nombre'],data['apellido'],data['nombreUsuario'],data['correo'],data['contrasena']))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
