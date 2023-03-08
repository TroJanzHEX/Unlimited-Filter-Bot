app.py


from flask import Flask
app = Flask(name)

@app.route('/')
def hello_world():
    return 'GreyMatters'


if name == "main":
    app.run()
