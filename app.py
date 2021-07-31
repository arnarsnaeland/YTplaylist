from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import op

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Song %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        YTplaylistURL = request.form['content']
        playlist = op.main(YTplaylistURL)
        dbPlaylist = []
        for song in playlist:
            dbPlaylist.append(Playlist(title = song))
        try:
            for song in dbPlaylist:
                db.session.add(song)
                db.session.commit()

            return redirect('/')
        except:
            return 'Error'
    else:
        playlist = Playlist.query.order_by(Playlist.date_created).all()
        return render_template('index.html', playlist = playlist)

if __name__ == "__main__":
    app.run(debug=True)