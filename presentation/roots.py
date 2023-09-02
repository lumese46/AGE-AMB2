from presentation import app

@app.route("/")
def index_page():
    return "hello_world"
