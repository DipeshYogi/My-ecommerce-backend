import psycopg2
import psycopg2.extras

class GetConnection():
  """
  Connect to postgres DB
  """
  def obtain_connection(self):
    try:
      conn = psycopg2.connect(
                  user = 'postgres',
                  password = 'CT0t1868',
                  host = 'localhost',
                  port = '5432',
                  database = 'BonoApeDb'
      )
      cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
      return conn, cursor

    except (Exception, psycopg2.Error) as error:
      print ("error while connecting to postgres", error)
  
  def close_connection(self, conn, cursor):
        conn.close()
        cursor.close()
        print("Connection Closed")

