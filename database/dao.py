from database.DB_connect import DBConnect
from model.spigoli import Spigolo
from model.user import User

class Dao:
    def __init__(self):
        pass

    @staticmethod
    def read_all_users():
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ SELECT * FROM Users """

        cursor.execute(query)

        for row in cursor:
            user = User(
                row["user_id"],
                row["votes_funny"],
                row["votes_useful"],
                row["votes_cool"],
                row["name"],
                row["average_stars"],
                row["review_count"]
            )

            results.append(user)

        cursor.close()
        cnx.close()

        return results

    @staticmethod
    def read_users_with_n_bus(n_bus, map_users):
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ 
                select r.user_id , count(*) as n_bus_reviewed
                    from reviews r 
                    group by r.user_id
                    having count(*)>= %s
                """

        cursor.execute(query, (n_bus, ))

        for row in cursor:
            id = row["user_id"]
            n_bus_reviewed = int(row["n_bus_reviewed"])
            map_users[id].n_bus_reviewed = n_bus_reviewed

            results.append(map_users[id])



        cursor.close()
        cnx.close()
        print(f'Nodi: {results}')
        return results


    @staticmethod
    def read_edges():
        print("Executing read from database using SQL query")

        results = []
        cnx = DBConnect.get_connection()

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)

        query = """ 
                with tab1 as(
                    select r.user_id , r.business_id 
                    from reviews r),
                    tab2 as(
                    select a.user_id id1, a.business_id bus1, b.user_id id2, b.business_id bus2
                    from tab1 a, tab1 b
                    where a.user_id > b.user_id and a.business_id = b.business_id)
                select id1, id2, count(*) as comuni
                from tab2
                group by id1, id2
                """

        cursor.execute(query)

        for row in cursor:
            spigolo = Spigolo(**row)
            results.append(spigolo)


        cursor.close()
        cnx.close()
        print(f'Spigoli non filtrati: {results}')
        return results

