import fnmatch
import os

from flask import Flask, request, send_file, jsonify, url_for, abort

from models import db, File

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cdn.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_HOSTS'] = ['*']

db.init_app(app)
with app.app_context():
    db.create_all()

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.before_request
def restrict_hosts():
    host = request.host.split(':')[0]
    flag = False
    for pattern in app.config['ALLOWED_HOSTS']:
        if fnmatch.fnmatch(host, pattern):
            flag = True
            break
    if not flag:
        abort(403)


@app.route('/files/<filename>', methods=['POST'])
def upload_file(filename):
    existing_file = File.query.filter_by(filename=filename).first()
    if existing_file:
        return jsonify({'status': 1, 'error': 'File already exists'}), 409
    file = request.files.get('file')
    if not file:
        return jsonify({'status': 1, 'error': 'Invalid request'}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        new_file = File(filename=filename, filepath=filepath)
        db.session.add(new_file)
        db.session.commit()
        file_url = url_for('get_file', filename=filename, _external=True)
        return jsonify({'status': 0, 'filepath': file_url}), 201
    except Exception as e:
        return jsonify({'status': 1, 'error': str(e)}), 500


@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    file = File.query.filter_by(filename=filename).first()
    if file is None:
        return jsonify({'status': 1, 'error': 'File not found'}), 404
    # set url arguments to download or open file in browser
    as_attachment = True if request.args.get("asattachment") == "1" else False
    return send_file(file.filepath, as_attachment=as_attachment), 200


@app.route('/files/<filename>', methods=['PUT'])
def replace_file(filename):
    file = File.query.filter_by(filename=filename).first()
    if not file:
        return jsonify({'status': 1, 'error': 'File not found'}), 404
    new_file = request.files.get('file')
    if not new_file:
        return jsonify({'status': 1, 'error': 'Invalid request'}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_file.save(filepath)
        file.filepath = filepath
        db.session.commit()
        file_url = url_for('get_file', filename=filename, _external=True)
        return jsonify({'status': 0, 'filepath': file_url}), 200
    except Exception as e:
        return jsonify({'status': 1, 'error': str(e)}), 500


@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file = File.query.filter_by(filename=filename).first()
    if not file:
        return jsonify({'status': 1, 'error': 'File not found'}), 404
    try:
        os.remove(filepath := file.filepath)
        db.session.delete(file)
        db.session.commit()
        return jsonify({'status': 0, 'filepath': filepath}), 200
    except Exception as e:
        return jsonify({'status': 1, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
