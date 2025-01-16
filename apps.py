from flask import Flask, jsonify
app = Flask(__name__)

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['target'] = iris.target

X= iris.data
y=iris.target

X_train, X_test, y_train, y_test =train_test_split(X, y,test_size=0.4, random_state=42)

clf= DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

@app.route("/get status", methods=["Get"])
def foo():
    return jsonify({"training":70, "testing":30})
if __name__ == "__main__":
    app.run()