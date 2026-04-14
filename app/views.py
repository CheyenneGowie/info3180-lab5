"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
from flask_wtf.csrf import generate_csrf
from app.forms import MovieForm
from app.models import Movie
import os




@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    title = request.form.get('title')
    description = request.form.get('description')
    poster_file = request.files.get('poster')

    errors = []
    if not title:
        errors.append("Title is required")
    if not description:
        errors.append("Description is required")
    if not poster_file:
        errors.append("Poster is required")

    if errors:
        return jsonify({'errors': errors}), 400

    from werkzeug.utils import secure_filename
    filename = secure_filename(poster_file.filename)

    upload_folder = os.path.join(os.getcwd(), 'app/uploads')
    os.makedirs(upload_folder, exist_ok=True)

    poster_file.save(os.path.join(upload_folder, filename))

    movie = Movie(title=title, description=description, poster=filename)
    db.session.add(movie)
    db.session.commit()

    return jsonify({
        'message': 'Movie Successfully added',
        'title': title,
        'poster': filename,
        'description': description
    }), 201



@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies_list = Movie.query.all()
    movies_data = []
    for movie in movies_list:
        movies_data.append({
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': f'http://localhost:8080/api/v1/posters/{movie.poster}'
        })
    return jsonify({'movies': movies_data})


@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    upload_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(os.path.join(os.getcwd(), upload_folder), filename)


###
# The functions below should be applicable to all Flask apps.
###

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify(error="Page Not Found"), 404