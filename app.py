from flask import Flask, request, jsonify, render_template
from main import main
import os   

app = Flask(__name__)

UPLOAD_FOLDER = 'src/csvManipulationFunctions/CSVs'
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdirs(UPLOAD_FOLDER)

@app.route('/')
def upload_menu():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_fileInfo():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        if 'info' not in request.form:
            return jsonify({'error': 'Nenhuma informação passada'}), 400
        info = request.form['info']
        main(info, file.filename)

        return jsonify({'message': 'File succsefully uploaded', 'file_path': file.filename, 'info': info}), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    