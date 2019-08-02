import pandas as pd
import numpy as np
import pickle
import os, io

from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'

@app.route('/', methods=['GET', 'POST'])
def predict():
    data = {"success": False}
    if request.method == 'POST':
        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            hr = pd.read_csv(filename)
            col_names = hr.columns.tolist()
            hr = hr.rename(columns = {'sales':'department'})

            cat_vars=['department','salary']
            for var in cat_vars:
                cat_list='var'+'_'+var
                cat_list = pd.get_dummies(hr[var], prefix=var)
                hr1=hr.join(cat_list)
                hr=hr1
          #if having issue with column, adjust this line.
            hr.drop(hr.columns[[7, 8]], axis=1, inplace=True)

            print(list(hr))

            prediction = model.predict(hr)

            print(prediction)

            data["predictions"] = []

            for prediction in prediction:
                r = {"Prediction": int(prediction)}
                data["predictions"].append(r)

                data["success"] = True

        return jsonify(data)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    model = pickle.load(open('model.pkl', 'rb'))
    app.run(debug=True)
