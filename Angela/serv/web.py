import os
from bson import ObjectId
from flask import Blueprint, jsonify, send_file, request,render_template
from Config import RET,MongoDB,COVER_PATH,MUSIC_PATH
webs = Blueprint("webs",__name__)
# b5b7ea5dc366cbb065b0fcb4a7f48bc8
@webs.route("/web",methods=["GET"])
def web():
    return render_template("WebToy.html")


