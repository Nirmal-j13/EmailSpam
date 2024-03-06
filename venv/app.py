from flask import Flask,jsonify,request
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask_cors import CORS
app=Flask(__name__)
CORS(app)


df=pd.read_csv("venv\mail_data.csv")
print(df)

data = df.where((pd.notnull(df)),'')

data.loc[data['Category']=='spam','Category',]=0
data.loc[data['Category']=='ham','Category',]=1

x=data['Message']
y=data['Category']

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=3)

feature_extraction = TfidfVectorizer(min_df=1,stop_words='english',lowercase=True)
x_train_features = feature_extraction.fit_transform(x_train)
x_test_features = feature_extraction.transform(x_test)
y_train = y_train.astype('int')
y_test = y_test.astype('int')

model = LogisticRegression()
model.fit(x_train_features,y_train)

prediction_on_training_data=model.predict(x_train_features)
accuracy_on_training_data=accuracy_score(y_train,prediction_on_training_data)

prediction_on_test_data=model.predict(x_test_features)
accuracy_on_test_data=accuracy_score(y_test,prediction_on_test_data)

@app.route('/',methods=['POST','GET'])
def home():
        prediction=""
        if request.method == 'POST':
                mail=request.get_json()
                print(mail)
                input_your_mail=[mail.get('mail')] 
                print(input_your_mail)
                input_data_features=feature_extraction.transform(input_your_mail)
                prediction=model.predict(input_data_features)
                prediction=str(prediction)
                print(prediction)
                return {"hamspam":prediction}
        elif request.method == 'GET':
                print(prediction)
                return {"hamspam":prediction}

if __name__ == '__main__':
    app.run(debug=True)