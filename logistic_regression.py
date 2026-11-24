import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix,f1_score
from sklearn.linear_model import LogisticRegression
a=pd.read_csv("data/student_dataset.csv")
a = a.drop(columns=["student_id"])

#separating the input and output features
x = a.iloc[:, :-1]
y = a["career_role"]
print(x.shape)
print(y.shape)

#train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,stratify=y)

#scaling
sc = StandardScaler()
x_train = pd.DataFrame(sc.fit_transform(x_train),columns=x_train.columns)
x_test = pd.DataFrame(sc.transform(x_test),columns=x_test.columns)  
print(x_train.shape)
print(x_test.shape)
#creating the model
lr=LogisticRegression(max_iter=1000,random_state=42)
lr.fit(x_train,y_train) 
y_pred=lr.predict(x_test)   
accuracy = accuracy_score(y_test, y_pred)
print(accuracy)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(f1_score(y_test,y_pred,average='weighted'))