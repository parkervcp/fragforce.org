from fragforce import app

@app.route('/')
def index(name=None):
  return render_template('index.html', name=name)
