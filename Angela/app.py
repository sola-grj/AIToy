from flask import Flask

from serv.content import content
from serv.users import user
from serv.Devices import devices
from serv.friends import friends
from serv.web import webs
from serv.toy import toy
from serv.Uploader import uploader
app = Flask(__name__)
app.debug = True
app.register_blueprint(content)
app.register_blueprint(user)
app.register_blueprint(devices)
app.register_blueprint(friends)
app.register_blueprint(webs)
app.register_blueprint(toy)
app.register_blueprint(uploader)

if __name__ == '__main__':
    app.run("0.0.0.0",9527)