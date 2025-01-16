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

X_train, X_test, y_train, y_test =train_test_split(X, y,test_size=0.6, random_state=42)

clf= DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt 
plt.figure(figsize = (12,8))
plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)
plt.title("DC MLOPS")
plt.show()
