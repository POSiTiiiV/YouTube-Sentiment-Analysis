from flask import Flask, request, render_template
from predict import predict_sentiments
from youtube import get_video_comments
from flask_cors import CORS
from flask import session

app = Flask(__name__)
app.secret_key = 'my_secret_key'
CORS(app)


def get_video(video_id):
    if not video_id:
        return {"error": "video_id is required"}

    comments = get_video_comments(video_id)
    predictions = predict_sentiments(comments)

    positive = predictions.count("Positive")
    negative = predictions.count("Negative")

    summary = {
        "positive": positive,
        "negative": negative,
        "num_comments": len(comments),
        "rating": (positive / len(comments)) * 100 if len(comments) != 0 else 0
    }

    return {"predictions": predictions, "comments": comments, "summary": summary}


@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    comments = []
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        video_id = video_url.split("v=")[1]
        data = get_video(video_id)

        summary = data['summary']
        comments = list(zip(data['comments'], data['predictions']))
        session['comments'] = comments
    return render_template('index.html', summary=summary)


@app.route('/newpage')
def newPage():
    comments = session.get('comments', [])  # retrieve the comments from the session
    return render_template('newpage.html', comments=comments)


if __name__ == '__main__':
    app.run(debug=True)
