import os
import psycopg2
import psycopg2.extras

class GetConnection():
  """
  Connect to postgres DB
  """
  def obtain_connection(self):
    try:
      if os.environ.get('DATABASE_URL'):
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
      else:
        conn = psycopg2.connect(os.environ.get('ECOM_DB'))

      cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
      return conn, cursor

    except (Exception, psycopg2.Error) as error:
      print ("error while connecting to postgres", error)
  
  def close_connection(self, conn, cursor):
        conn.close()
        cursor.close()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    "Return one row from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))

       

