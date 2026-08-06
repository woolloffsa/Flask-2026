from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)
DATABASE = "DigiCloset.db"

def create_connection(db_file):
  """Creates a connection to the database
  :parameter db_file - name of the file
  :returns connection - a connection to the database
  """
  try:
    connection = sqlite3.connect(db_file)
    return connection
  except Error as e:
    print(e)
  return None


@app.route('/')
def render_home():
    return render_template("index.html")


@app.route('/inventory')
def render_inventory():
  query = "SELECT clothing_type, colour FROM closet"
  con = create_connection(DATABASE)
  cur = con.cursor()

  cur.execute(query)
  clothing_list = cur.fetchall()
  con.close()
  print(clothing_list)
  return render_template("inventory.html", clothes=clothing_list)


@app.route('/outfits')
def render_outfits():
  return render_template("outfits.html")


if __name__ == '__main__':
  app.run()