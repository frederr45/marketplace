from flask import Blueprint, send_from_directory, current_app


blueprint = Blueprint('img', __name__)

# Какой URL он подкладывает. hekp
@blueprint.route('/hekp/<path:filename>')
def send_file(filename):
    return send_from_directory(f'{current_app.static_folder}/static', filename)
# Куда он смотрит на самом деле
@blueprint.route('/hekp/uploaded/<path:filename>')
def send_picture(filename):
    return send_from_directory(
        f'{current_app.static_folder}/uploaded', filename)

@blueprint.route('/hekp/numbers/<path:filename>')
def send_number(filename):
    return send_from_directory(
        f'{current_app.static_folder}/numbers', filename)
