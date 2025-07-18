from dotenv import load_dotenv
import os
from peewee import *
from flask import Flask, render_template, request
from data.profiles import profiles
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(
        name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_time_line_post(id):
    post = TimelinePost.get_or_none(TimelinePost.id == id)
    if not post:
        return {'status': 'error', 'message': 'Post not found'}, 404
    post.delete_instance()
    return {'status': 'success', 'message': 'Post deleted successfully'}, 200


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellows", url=os.getenv("URL"), profiles=profiles)


@app.route('/hobbies/<name>')
def hobbies(name):
    profile = next(
        (p for p in profiles if p["name"].lower().replace(" ", "-") == name), None
    )
    return render_template(
        "hobbies.html",
        profile=profile,
        title=profile["name"],
        url=os.getenv("URL"),
        profiles=profiles,
    )


@app.route('/about/<name>')
def about_profile(name):
    profile = next(
        (p for p in profiles if p['name'].lower().replace(" ", "-") == name), None)
    return render_template('about_page.html',
                           profile=profile,
                           title=profile['name'],
                           url=os.getenv("URL"),
                           profiles=profiles)


@app.route('/timeline')
def timeline():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return render_template('timeline.html', title="Timeline", posts=posts)
