from flask import Flask, render_template

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

@app.route('/')
def render_home():
    return render_template("index.html")


@app.route('/inventory')
def render_inventory():
  return render_template("inventory.html")


@app.route('/outfits')
def render_outfits():
  return render_template("outfits.html")


if __name__ == '__main__':
  app.run()