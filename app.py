from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

DATABASE = "CyberStyle.db"

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
  # Get the sort request, default to 'clothing_id' if not provided
  sort = request.args.get('sort', 'clothing_id')
  # Get the current sort order, default to 'asc' if not provided
  order = request.args.get('order', 'asc')

  # Toggle the sort order
  if order == 'asc':
    new_order = 'desc'
  else:
    new_order = 'asc'

  con = create_connection(DATABASE)
  cur = con.cursor()
  # Sort query
  query = "SELECT clothing_type, colour, weather, image FROM closet ORDER BY " + sort + " " + order
  # Query the db for the sorted fields
  cur.execute(query)
  clothing_list = cur.fetchall()
  con.close()
  return render_template("inventory.html", clothes=clothing_list, order=new_order)


@app.route('/outfits')
def render_outfits():
  return render_template("outfits.html")
  

@app.route('/search', methods=['GET', 'POST'])
def render_search():
  """
  Function to find all the records which contain the search item
  :parameters
  :POST contains the search value
  :returns a rendered page
  """
  search = request.form['search']

  # Search query
  query = """
        SELECT * FROM closet 
        WHERE clothing_id LIKE ?
           OR clothing_type LIKE ?
           OR colour LIKE ?
           OR weather LIKE ?
    """

  con = create_connection(DATABASE)
  cur = con.cursor()
  # Query the db for any matches of search
  cur.execute(query, (search, search, search, search))
  clothing_list = cur.fetchall()
  con.close()
  return render_template("index.html", clothes=clothing_list)


if __name__ == '__main__':
  app.run()