import pymysql

class DAOEstudiante:
    def connect(self):
        return pymysql.connect(host="localhost",user="root",password="",db="db_poo" )

    def read(self, id):
        con = DAOEstudiante.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM registro_estudiantes order by nombre asc")
            else:
                cursor.execute("SELECT * FROM registro_estudiantes where id = %s order by nombre asc", (id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,data):
        con = DAOEstudiante.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("INSERT INTO registro_estudiantes(nombre,apellido,username,contrasena) VALUES(%s, %s, %s,%s)", (data['nombre'],data['apellido'],data['username'],data['contrasena'],))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
