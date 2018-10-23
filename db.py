import mysql.connector

class DB:
    def __init__(self, host, user, password):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__connexion = mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            passwd=self.__password
        )

    def select_all_shapes(self):
        cursor = self.__connexion.cursor()
        query = "SELECT * FROM SHAPES"
        cursor.execute(query)
        shapes = []
        for (type, x1, y1, x2, y2, fill) in cursor:
            shapes.append({
                "type": type,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "fill": fill
            })
        return shapes

    def insert_shape(self, shape):
        cursor = self.__connexion.cursor()
        query = "INSERT INTO SHAPES(type,x1,y1,x2,y2,fill) VALUES (%s,%s,%s,%s,%s,%s)"
        type = shape["type"]
        x1 = shape["x1"]
        y1 = shape["y1"]
        x2 = shape["x2"]
        y2 = shape["y2"]
        fill = shape["fill"]
        cursor.execute(query, (type, x1, y1, x2, y2, fill))
