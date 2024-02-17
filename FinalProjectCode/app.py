from flask import Flask,render_template,send_file,flash,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
from functionality import *
from datetime import datetime

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#def create_app():
app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def upload():
    return render_template('main.html')

@app.route('/download')
def download_file():
   path = "downloads/answer.csv"
   return send_file(path,as_attachment=True)

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        files = os.listdir('uploads/')
        for file in files:
            os.remove("uploads/"+file)
        
        files = os.listdir('downloads/')
        for file in files:
            os.remove("downloads/"+file)

        inpfile = request.files['file']
        if inpfile and inpfile.filename != '' and allowed_file(inpfile.filename):
            secureinpfilename = secure_filename(inpfile.filename)
            save_location = os.path.join('uploads',secureinpfilename)
            inpfile.save(save_location)

            filenum = process_csv(save_location)

        #return redirect(url_for('download'))
        #return 'uploaded'
    #return redirect(url_for('/result'))   
    return render_template('result.html')


if __name__ == "__main__":
    app.run(debug=True,port=8000)


