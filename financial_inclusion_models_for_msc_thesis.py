# -*- coding: utf-8 -*-
"""Financial Inclusion Models for Msc Thesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q7UEFR1QSJXEKLBU8CYtehL47V_D3dqw
"""

#from google.colab import drive
#drive.mount('/content/drive')

#cd drive/"My Drive"/Research/

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns                       #visualisation
import matplotlib.pyplot as plt             #visualisation
# %matplotlib inline
sns.set(color_codes=True)
import pandas.util.testing as tm
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from xgboost import XGBClassifier
from xgboost import plot_tree

import tensorflow as tf
from tensorflow import keras

from tensorflow.keras import layers
from tensorflow.keras.layers import IntegerLookup
from tensorflow.keras.layers import Normalization
from tensorflow.keras.layers import StringLookup


import os
import tempfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import sklearn
from sklearn.preprocessing import StandardScaler

from google.colab import files
data_to_load = files.upload()

import io
df = pd.read_csv(io.BytesIO(data_to_load['Financial_Inclusion_Final_Dataset.csv']))

df.head()

print(df.describe())

df.dtypes

df.describe(include='all')

def reload_dataset():
  import io
  from sklearn.linear_model import LogisticRegression
  from sklearn.model_selection import train_test_split

  df = pd.read_csv(io.BytesIO(data_to_load['Financial_Inclusion_Final_Dataset.csv']))
  df.drop(['Survey_Year'], axis=1, inplace=True)

  #Create Dummy Variables
  df_encoded = pd.get_dummies(df, drop_first=True)

  #Balancing the Dataset - Undersampling

  ## Get the Banked and the Unbanked dataset
  df_encoded_banked = df_encoded[df_encoded['Bank_Status']==1]
  df_encoded_unbanked = df_encoded[df_encoded['Bank_Status']==0]

  # Class count
  count_df_encoded_unbanked, count_df_encoded_banked = df_encoded.Bank_Status.value_counts()

  # Random Undersampling
  df_encoded_unbanked_under = df_encoded_unbanked.sample(count_df_encoded_banked)
  df_encoded_under = pd.concat([df_encoded_unbanked_under, df_encoded_banked], axis=0)

  print('Random under-sampling:')
  print(df_encoded_under.Bank_Status.value_counts())
  return df_encoded_under

reload_dataset()

from sklearn.metrics import confusion_matrix
def perf_measure(actual, prediction):
  TN, FP, FN, TP = confusion_matrix(actual, prediction).ravel()

  # Sensitivity, hit rate, recall, or true positive rate
  TPR = round(TP/(TP+FN),3)
  print('Sensitivity, hit rate, recall, or true positive rate - TPR: {:.2f}'.format(TPR))

  # Specificity or true negative rate
  TNR = round(TN/(TN+FP),3)
  print('Specificity or true negative rate - TNR: {:.2f}'.format(TNR))

  # Precision or positive predictive value
  PPV = round(TP/(TP+FP),3)
  print('Precision or positive predictive value - PPV: {:.2f}'.format(PPV))

  # Negative predictive value
  NPV = round(TN/(TN+FN),3)
  print('Negative predictive value - NPV: {:.2f}'.format(NPV))

  # Fall out or false positive rate
  FPR = round(FP/(FP+TN),3)
  print('Fall out or false positive rate - FPR: {:.2f}'.format(FPR))

  # False negative rate
  FNR = round(FN/(TP+FN),3)
  print('False negative rate - FNR: {:.2f}'.format(FNR))

  # False discovery rate
  FDR = round(FP/(TP+FP),3)
  print('False discovery rate - FDR: {:.2f}'.format(FDR))

  # Overall accuracy
  ACC = round((TP+TN)/(TP+FP+FN+TN),3)
  print('Overall accuracy - ACC: {:.2f}'.format(ACC))

  return (TPR, TNR, PPV, NPV, FPR, FDR, ACC)

"""# Data Exploration"""

df.head()

df.info()

df.describe()

list(set(df.dtypes.tolist()))

df_num = df.select_dtypes(include = ['float64', 'int64'])
df_num.head()

df_num.hist(figsize=(16, 20), bins=50, xlabelsize=8, ylabelsize=8);

df.drop(['Survey_Year'], axis=1, inplace=True)
df.head()

# find categorical variables
categorical = [var for var in df.columns if df[var].dtype=='O']
print('There are {} categorical variables\n'.format(len(categorical)))
print('The categorical variables are :', categorical)

# view the categorical variables
df[categorical].head()

# check missing values in categorical variables
df[categorical].isnull().sum()

# print categorical variables containing missing values
cat1 = [var for var in categorical if df[var].isnull().sum()!=0]
print(df[cat1].isnull().sum())

# view frequency distribution of categorical variables

# for var in categorical:
#    print(df[var].value_counts()/np.float(len(df)))

# check for cardinality in categorical variables
for var in categorical:
    print(var, ' contains ', len(df[var].unique()), ' labels')

# print number of labels in Location variable
print('States contains', len(df.State.unique()), 'labels')

# check labels in location variable
df.State.unique()

print(np.sort(df.State.unique()))

df.Sector.unique()

df.Gender.unique()

df.Marital_status.unique()

"""# EDA - Data Visualization"""

sns.countplot(x='Bank_Status', data=df)

fig, ax = plt.subplots(figsize=(10,12))
sns.countplot(x='Bank_Status',  data=df)
for container in ax.containers:
    ax.bar_label(container)

fig, ax = plt.subplots(figsize=(20,12))
sns.heatmap(df.corr(), annot = True, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm', annot_kws={"size":18})
plt.title("Correlation matrix of Numerical Features in dataset", y=-0.75)
plt.xlabel("Financial Inclusion Features")
plt.ylabel("Financial Inclusion Features")
plt.show()

fig, ax = plt.subplots(figsize=(22,15))
sns.set_theme(style="white", font_scale=2.0)

sns.heatmap(df.corr(), annot = True, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm', annot_kws={"size":20, "fontweight": 'bold'})
#plt.title("Correlation matrix of Numerical Features in dataset", y=-0.25)
plt.xlabel("Financial Inclusion Features", fontsize=18);
plt.ylabel("Financial Inclusion Features", fontsize=18);
plt.show()
fig.savefig('Corrs.jpg', bbox_inches="tight")

fig, ax = plt.subplots(figsize=(10,12))
sns.countplot(x='Bank_Status', hue='Residential_Area_Density', data=df)

fig, ax = plt.subplots(figsize=(10,12))
sns.countplot(x='Bank_Status', hue='Residential_Area_Density', data=df)
for container in ax.containers:
    ax.bar_label(container)

fig, ax = plt.subplots(figsize=(10,4))
sns.countplot(x='Bank_Status', hue='Education_Level', data=df)

plt.hist(df['Age'].dropna())

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

table=pd.crosstab(df.State , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of State vs Banked Adults')
plt.xlabel('State')
plt.ylabel('Proportion of States')
plt.savefig('Education_Level_vs_banked')

table=pd.crosstab(df.Sector , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=False, figsize=(15, 10))
plt.title('Stacked Bar Chart of Sector vs Banked Adults')
plt.xlabel('Sector')
plt.ylabel('Proportion of Sector')
plt.savefig('Sector_vs_banked')

fig, ax = plt.subplots(figsize=(10,12))
sns.countplot(x='Bank_Status', hue='Sector', data=df)
for container in ax.containers:
    ax.bar_label(container)

table=pd.crosstab(df.Residential_Area_Density	 , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=False, figsize=(15, 10))
plt.title('Stacked Bar Chart of Residential_Area_Density vs Banked Adults')
plt.xlabel('Residential_Area_Density')
plt.ylabel('Proportion of Residential_Area_Density')
plt.savefig('Residential_Area_Density_vs_banked')

pd.crosstab(df.Gender,df.Bank_Status).plot(kind='bar', stacked=False, figsize=(15, 10))
plt.title('Gender Frequency for Bank Status')
plt.xlabel('Gender')
plt.ylabel('Frequency of State')
plt.savefig('Gender_fre_job')

table=pd.crosstab(df.Marital_status , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of Marital Status vs Banked Adults')
plt.xlabel('Marital Status')
plt.ylabel('Proportion of Banked Adults')
plt.savefig('mariral_vs_banked')

table=pd.crosstab(df.Employment_Status , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of Employment_Status vs Banked Adults')
plt.xlabel('Employment_Status')
plt.ylabel('Proportion of Banked Adults')
plt.savefig('Employment_Status_vs_banked')

table=pd.crosstab(df.Monthly_Income_Rank	 , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of Monthly_Income_Rank	 vs Banked Adults')
plt.xlabel('Monthly_Income_Rank	')
plt.ylabel('Proportion of Banked Adults')
plt.savefig('Monthly_Income_Rank_vs_banked')

table=pd.crosstab(df.Education_Level , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of Education Level vs Banked Adults')
plt.xlabel('Education Level')
plt.ylabel('Proportion of Banked Adults')
plt.savefig('Education_Level_vs_banked')

table=pd.crosstab(df.Occupation_Score , df.Bank_Status)
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True, figsize=(15, 10))
plt.title('Stacked Bar Chart of Occupation Score vs Banked Adults')
plt.xlabel('Occupation_Score')
plt.ylabel('Proportion of Banked Adults')
plt.savefig('Occupation_Score_vs_banked')

pd.crosstab(df.Access_to_Mobile_Phone	,df.Bank_Status).plot(kind='bar', stacked=False, figsize=(3, 8))
plt.title('Bank Status distribution over Access_to_Mobile_Phone')
plt.xlabel('Access_to_Mobile_Phone	')
plt.ylabel('Frequency of Adult Population with Access_to_Mobile_Phone')
plt.savefig('Access_to_Mobile_Phone	_fre_job')

fig, ax = plt.subplots(figsize=(10,12))
sns.countplot(x='Bank_Status', hue='Access_to_Mobile_Phone', data=df)
for container in ax.containers:
    ax.bar_label(container)

pd.crosstab(df.Access_to_Personal_Computer	,df.Bank_Status).plot(kind='bar', stacked=False, figsize=(3, 8))
plt.title('Bank Status distribution over Access_to_Personal_Computer')
plt.xlabel('Access_to_Personal_Computer')
plt.ylabel('Frequency of Adult Population with Access_to_Personal_Computer')
plt.savefig('Access_to_Personal_Computer_Phone_fre_job')

pd.crosstab(df.Access_to_Internet_or_Email, df.Bank_Status).plot(kind='bar', stacked=False, figsize=(3, 8))
plt.title('Bank Status distribution over Access_to_Internet_or_Email')
plt.xlabel('Access_to_Internet_or_Email')
plt.ylabel('Frequency of Adult Population with Access_to_Internet_or_Email')
plt.savefig('Access_to_Internet_or_Email_fre_job')

pd.crosstab(df.Access_to_Television	, df.Bank_Status).plot(kind='bar', stacked=False, figsize=(3, 8))
plt.title('Bank Status distribution over Access_to_Television	')
plt.xlabel('Access_to_Television	')
plt.ylabel('Frequency of Adult Population with Access_to_Television	')
plt.savefig('Access_to_Television_fre_job')

#df.head()

"""# Building the Baseline Classification Model using Logistic Regression"""

# Create Dummy Variables
df_encoded = pd.get_dummies(df, drop_first=True)

X = df_encoded.loc[:, df_encoded.columns != 'Bank_Status']
y = df_encoded.loc[:, df_encoded.columns == 'Bank_Status']
X.head()

# split X and y into training and testing sets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
print(len(y_test))
print(len(y_pred))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

print(X_train.shape)
print(X_test.shape)

"""*** Model Evaluation ***"""

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

# confusion Matrix
conf_matrix=pd.DataFrame(data=confusion_matrix,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu");
conf_matrix

from sklearn.metrics import confusion_matrix
def perf_measure(actual, prediction):
  TN, FP, FN, TP = confusion_matrix(actual, prediction).ravel()

  # Sensitivity, hit rate, recall, or true positive rate
  TPR = round(TP/(TP+FN),3)
  print('Sensitivity, Recall, or True Positive Rate - TPR: {:.2f}'.format(TPR))

  # Specificity or true negative rate
  TNR = round(TN/(TN+FP),3)
  print('Specificity or True Negative Rate - TNR:          {:.2f}'.format(TNR))

  # Precision or positive predictive value
  PPV = round(TP/(TP+FP),3)
  print('Precision or Positive Predictive Value - PPV:     {:.2f}'.format(PPV))

  # Negative predictive value
  NPV = round(TN/(TN+FN),3)
  print('Negative Predictive Value - NPV:                  {:.2f}'.format(NPV))

  # Fall out or false positive rate
  FPR = round(FP/(FP+TN),3)
  print('Fall Out or False Positive Rate - FPR:            {:.2f}'.format(FPR))

  # False negative rate
  FNR = round(FN/(TP+FN),3)
  print('False Negative Rate - FNR:                        {:.2f}'.format(FNR))

  # False discovery rate
  FDR = round(FP/(TP+FP),3)
  print('False Discovery Rate - FDR:                       {:.2f}'.format(FDR))

  # Overall accuracy
  ACC = round((TP+TN)/(TP+FP+FN+TN),3)
  print('Overall Accuracy - ACC:                           {:.2f}'.format(ACC))

  return (TPR, TNR, PPV, NPV, FPR, FDR, ACC)

print('Test - Logistic Regression Model Measure')
perf_measure(y_test, y_pred)

#count_df_encoded_unbanked, count_df_encoded_banked

"""#Balancing the Dataset - Undersampling"""

## Get the Banked and the Unbanked dataset
df_encoded_banked = df_encoded[df_encoded['Bank_Status']==1]
df_encoded_unbanked = df_encoded[df_encoded['Bank_Status']==0]

sns.countplot(x='Bank_Status', data=df_encoded)

print(df_encoded_banked.shape,df_encoded_unbanked.shape)

"""*** Random Undersampling ***"""

reload_dataset()

"""### Model 1: Logistic Regression ###"""

# making a Logistic Regression on the Undersampled Data
df_encoded_under = reload_dataset()

X = df_encoded_under.loc[:, df_encoded_under.columns != 'Bank_Status']
y = df_encoded_under.loc[:, df_encoded_under.columns == 'Bank_Status']

#X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)
X_encoded_under_train, X_encoded_under_test, y_encoded_under_train, y_encoded_under_test = train_test_split(X, y, test_size=0.25, random_state=0)

logreg2 = LogisticRegression()
logreg2.fit(X_encoded_under_train, y_encoded_under_train)

print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg2.score(X_encoded_under_test, y_encoded_under_test)))
y_encoded_under_pred = logreg.predict(X_encoded_under_test)

#logreg.summary()

from sklearn.metrics import confusion_matrix
confusion_matrix2 = confusion_matrix(y_encoded_under_test, y_encoded_under_pred)
print(confusion_matrix2)

conf_matrix=pd.DataFrame(data=confusion_matrix2,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu");

print(classification_report(y_encoded_under_test, y_encoded_under_pred))

logit_roc_auc = roc_auc_score(y_encoded_under_test, logreg2.predict(X_encoded_under_test))
fpr, tpr, thresholds = roc_curve(y_encoded_under_test, logreg.predict_proba(X_encoded_under_test)[:,1])
plt.figure(figsize = (10,8))
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

print('Model #1 - Logistic Regression Model Measure - Using Undersampled Data:')
perf_measure(y_encoded_under_test, logreg2.predict(X_encoded_under_test))

"""*** Over Sampling Method using SMOTE ***"""

# Over Sampling Method using SMOTE
from imblearn.over_sampling import SMOTE
smote = SMOTE()

#X_encoded_under_train, X_encoded_under_test, y_encoded_under_train, y_encoded_under_test = train_test_split(X, y, test_size=0.25, random_state=0)

X_train_smote, y_train_smote = smote.fit_resample(X_train.astype('float'),y_train)

X = df_encoded.loc[:, df_encoded.columns != 'Bank_Status']
y = df_encoded.loc[:, df_encoded.columns == 'Bank_Status']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

y_train.shape

from collections import Counter

print("Before SMOTE :" , Counter(y_train))
print("After SMOTE :" , Counter(y_train_smote))

# Over-sampling
print('Over-sampling:')
print(y_train_smote.Bank_Status.value_counts())

"""*** Making a Logistic Regression on the Over-sampled Data ***"""

logreg3 = LogisticRegression()
logreg3.fit(X_train_smote, y_train_smote)

y_smote_pred = logreg3.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg3.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix3 = confusion_matrix(y_test, y_smote_pred)
print(confusion_matrix3)

conf_matrix=pd.DataFrame(data=confusion_matrix3,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix, annot=True,fmt='d',cmap="YlGnBu");

logit_roc_auc = roc_auc_score(y_test, logreg3.predict(X_test))
fpr, tpr, thresholds = roc_curve(y_test, logreg3.predict_proba(X_test)[:,1])
plt.figure(figsize = (10,8))
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve for Logistic Regression Model')
plt.legend(loc="lower right")
plt.savefig('Log_ROC')
plt.show()

print(classification_report(y_test, y_smote_pred))

"""1.x - Logistic Regression Model Measure - Using Over-sampled Data"""

perf_measure(y_test, y_smote_pred)

"""### Model 2. Using Naive Baise

Still Working with our undersampled data
"""

reload_dataset()

"""Re preparing the dataset - for - Naive Bias Model"""

X = df_encoded_under.loc[:, df_encoded_under.columns != 'Bank_Status']
y = df_encoded_under.loc[:, df_encoded_under.columns == 'Bank_Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

#Import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB

#Create a Gaussian Classifier
gnb = GaussianNB()

#Train the model using the training sets
gnb.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = gnb.predict(X_test)

from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

from sklearn.metrics import confusion_matrix
confusion_matrix_gauss = confusion_matrix(y_test, y_pred)
print(confusion_matrix_gauss)

conf_matrix_gauss =pd.DataFrame(data=confusion_matrix_gauss,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix_gauss, annot=True,fmt='d',cmap="YlGnBu");

Y_gnb_score = gnb.predict_proba(X_test)

gnb_roc_auc = roc_auc_score(y_test, y_pred)
fpr, tpr, thresholds = roc_curve(y_test, Y_gnb_score[:, 1])
plt.figure(figsize = (10,8))
plt.plot(fpr, tpr, label='Naive Bayes Classification (area = %0.2f)' % gnb_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve for Naive Bayes Classification Model')
plt.legend(loc="lower right")
plt.savefig('NBG_ROC')
plt.show()

print(classification_report(y_test, y_pred))

perf_measure(y_test, y_pred)



"""### Model 3. Extreme Gradient Boosting - xGBoost Model"""



#Loading the data
sns.countplot(x='Bank_Status', data=df_encoded_under)
df_encoded_under = reload_dataset()
df_encoded_under.reset_index(drop=True, inplace=True)

type(df_encoded_under)

sns.countplot(x='Bank_Status', data=df_encoded_under)

X = df_encoded_under.loc[:, df_encoded_under.columns != 'Bank_Status']
y = df_encoded_under.loc[:, df_encoded_under.columns == 'Bank_Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

import xgboost as xgb
xgb_cl = xgb.XGBClassifier()

# Fit
xgb_cl.fit(X_train, y_train)

# Predict
preds = xgb_cl.predict(X_test)

# Score
accuracy_score(y_test, preds)

xgb_cl

from sklearn import metrics
print("Accuracy:",metrics.accuracy_score(y_test, preds))

from sklearn.metrics import confusion_matrix
confusion_matrix_xgb = confusion_matrix(y_test, preds)
print(confusion_matrix_xgb)

conf_matrix_xgb =pd.DataFrame(data=confusion_matrix_xgb,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix_xgb, annot=True,fmt='d',cmap="YlGnBu");

Y_xgb_score = xgb_cl.predict_proba(X_test)

xgb_roc_auc = roc_auc_score(y_test, preds)
fpr, tpr, thresholds = roc_curve(y_test, Y_xgb_score[:, 1])
plt.figure(figsize = (10,8))
plt.plot(fpr, tpr, label='Extreme Gradient Boosting - xGBoost Model (area = %0.2f)' % xgb_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve for Extreme Gradient Boosting - xGBoost Classification Model')
plt.legend(loc="lower right")
plt.savefig('XGB_ROC')
plt.show()

pip install dalex

import dalex as dx
dx.__version__

"""

```
# This is formatted as code
```


## create an explainer for the model¶"""

exp = dx.Explainer(xgb_cl, X, y)

vi = exp.model_parts()
vi.result

exp.predict(X)
exp.model_parts().plot()

exp.model_performance(model_type='classification').plot(geom='roc')

exp.model_parts().plot()

class Wrapper:
    def __init__(self, model):
        self.model = model

    def predict(self, dmatrix):
        return self.model.predict(dmatrix)

#exp.predict_parts(X.iloc[1000, :]).plot(min_max=[0,1])

#df = df_encoded_under

#(df_encoded_under.iloc[1,:])
#df.loc[df['Bank_Status'] == 1]

#df.reset_index(drop=True, inplace=True)

#df.loc[df['Bank_Status'] != 3]

#print(X.iloc[3, :])
print(y.iloc[3, :])
X.iloc[[3, ],:]

test1 = (X.iloc[[3, ],:])
#test1
#bd_test1 = exp.predict_parts(test1, type='break_down', label=test1.index[0])

bd_test1 = exp.predict_parts(test1, type='break_down', label=test1.index[0])
bd_interactions_test1 = exp.predict_parts(test1, type='break_down_interactions', label="Bank_Status0")
#
#bd_test1.result

#exp.predict_parts(X.iloc[0, :]).plot(min_max=[0,1])
bd_test1.plot(bd_interactions_test1)

print(X.iloc[50027, :])
print(y.iloc[50027, :])
X.iloc[[50027],:]

df_encoded_under.iloc[[50027, 50036],:]

X.tail(25)





# plot single tree
# from sklearn import tree

# tree.plot_tree(xgb_cl.fit(X_train, y_train))
# plt.show()

print(classification_report(y_test, preds))

perf_measure(y_test, preds)

hyhjhjh

"""### Warning do not Run ###

*** Optimizing the model using GridSearch ***
"""

param_grid = {
    "max_depth": [3, 4, 5, 7],
    "learning_rate": [0.1, 0.01, 0.05],
    "gamma": [0, 0.25, 1],
    "reg_lambda": [0, 1, 10],
    "scale_pos_weight": [1, 3, 5],
    "subsample": [0.8],
    "colsample_bytree": [0.5],
}

from sklearn.model_selection import GridSearchCV

# Init classifier
xgb_cl = xgb.XGBClassifier(objective="binary:logistic")

# Init Grid Search
## grid_cv = GridSearchCV(xgb_cl, param_grid, n_jobs=-1, cv=3, scoring="roc_auc")

# Fit
## _ = grid_cv.fit(X, y)

#grid_cv.best_score_

#grid_cv.best_params_

best_params_0 = {'colsample_bytree': 0.5,
 'gamma': 0.25,
 'learning_rate': 0.1,
 'max_depth': 7,
 'reg_lambda': 1,
 'scale_pos_weight': 3,
 'subsample': 0.8}

best_params_1= {'colsample_bytree': 0.5,
 'gamma': 0,
 'learning_rate': 0.05,
 'max_depth': 3,
 'reg_lambda': 0,
 'scale_pos_weight': 1,
 'subsample': 0.8}

best_params_1

final_cl = xgb.XGBClassifier(base_score=0.5, gamma=0,
              learning_rate=0.05, max_depth=3,
              reg_lambda=0, scale_pos_weight=1, subsample=0.8)

from sklearn.metrics import roc_auc_score
_ = final_cl.fit(X_train, y_train)
preds2 = final_cl.predict(X_test)

# Score
accuracy_score(y_test, preds)

confusion_matrix_xgb2 = confusion_matrix(y_test, preds)
print(confusion_matrix_xgb2)

# conf_matrix_xgb2 =pd.DataFrame(data=confusion_matrix_xgb2,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
# plt.figure(figsize = (10,8))
# sns.heatmap(conf_matrix_xgb2, annot=True,fmt='d',cmap="YlGnBu");

# Y_xgb_score2 = final_cl.predict_proba(X_test)

# xgb_roc_auc2 = roc_auc_score(y_test, preds2)
# fpr, tpr, thresholds = roc_curve(y_test, Y_xgb_score2[:, 1])
# plt.figure()
# plt.plot(fpr, tpr, label='Extreme Gradient Boosting - xGBoost Model (area = %0.2f)' % xgb_roc_auc2)
# plt.plot([0, 1], [0, 1],'r--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic curve for Extreme Gradient Boosting - xGBoost Classification Model')
# plt.legend(loc="lower right")
# plt.savefig('XGB_ROC')
# plt.show()

# print(classification_report(y_test, preds2))

# perf_measure(y_test, preds2)



"""### Model 4. Neural Network Using TensorFlow

### DNN Model with TensorFlow and Keras ##
"""

#Loading the data
cleaned_df = reload_dataset()

cleaned_df.head()

# Use a utility from sklearn to split and shuffle your dataset.
train_df, test_df = train_test_split(cleaned_df, test_size=0.2)
train_df, val_df = train_test_split(train_df, test_size=0.2)

# Form np arrays of labels and features.
train_labels = np.array(train_df.pop('Bank_Status'))
bool_train_labels = train_labels != 0
val_labels = np.array(val_df.pop('Bank_Status'))
test_labels = np.array(test_df.pop('Bank_Status'))

train_features = np.array(train_df)
val_features = np.array(val_df)
test_features = np.array(test_df)

"""Normalize the input features using the sklearn StandardScaler. This will set the mean to 0 and standard deviation to 1."""

scaler = StandardScaler()
train_features = scaler.fit_transform(train_features)

val_features = scaler.transform(val_features)
test_features = scaler.transform(test_features)

train_features = np.clip(train_features, -5, 5)
val_features = np.clip(val_features, -5, 5)
test_features = np.clip(test_features, -5, 5)


print('Training labels shape:', train_labels.shape)
print('Validation labels shape:', val_labels.shape)
print('Test labels shape:', test_labels.shape)

print('Training features shape:', train_features.shape)
print('Validation features shape:', val_features.shape)
print('Test features shape:', test_features.shape)

"""## Define the model and metrics

Define a function that creates a simple neural network with a densly connected hidden layer, a dropout layer to reduce overfitting, and an output sigmoid layer that returns the probability of a transaction being fraudulent:
"""

mpl.rcParams['figure.figsize'] = (12, 10)
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

METRICS = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'),
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
      keras.metrics.AUC(name='prc', curve='PR'), # precision-recall curve
]

def make_model(metrics=METRICS, output_bias=None):
  if output_bias is not None:
    output_bias = tf.keras.initializers.Constant(output_bias)
  model = keras.Sequential([
      keras.layers.Dense(
          16, activation='relu',
          input_shape=(train_features.shape[-1],)),
      keras.layers.Dropout(0.5),
      keras.layers.Dense(1, activation='sigmoid',
                         bias_initializer=output_bias),
  ])

  model.compile(
      optimizer=keras.optimizers.Adam(learning_rate=1e-3),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model

#Build the Model
EPOCHS = 100
BATCH_SIZE = 2048

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_prc',
    verbose=1,
    patience=10,
    mode='max',
    restore_best_weights=True)

model = make_model()
model.summary()

model.predict(train_features[:10])

results = model.evaluate(train_features, train_labels, batch_size=BATCH_SIZE, verbose=0)
print("Loss: {:0.4f}".format(results[0]))

model = make_model()
#model.load_weights(initial_weights)
model.layers[-1].bias.assign([0.0])
zero_bias_history = model.fit(
    train_features,
    train_labels,
    batch_size=BATCH_SIZE,
    epochs=20,
    validation_data=(val_features, val_labels),
    verbose=0)

model = make_model()
#model.load_weights(initial_weights)
careful_bias_history = model.fit(
    train_features,
    train_labels,
    batch_size=BATCH_SIZE,
    epochs=20,
    validation_data=(val_features, val_labels),
    verbose=0)

def plot_loss(history, label, n):
  # Use a log scale on y-axis to show the wide range of values.
  plt.semilogy(history.epoch, history.history['loss'],
               color=colors[n], label='Train ' + label)
  plt.semilogy(history.epoch, history.history['val_loss'],
               color=colors[n], label='Val ' + label,
               linestyle="--")
  plt.xlabel('Epoch')
  plt.ylabel('Loss')

plot_loss(zero_bias_history, "Zero Bias", 0)
plot_loss(careful_bias_history, "Careful Bias", 1)

model = make_model()
#model.load_weights(initial_weights)
baseline_history = model.fit(
    train_features,
    train_labels,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=[early_stopping],
    validation_data=(val_features, val_labels))

"""## Check training history
In this section, you will produce plots of your model's accuracy and loss on the training and validation set. These are useful to check for overfitting
"""

def plot_metrics(history):
  metrics = ['loss', 'prc', 'precision', 'recall']
  for n, metric in enumerate(metrics):
    name = metric.replace("_"," ").capitalize()
    plt.subplot(2,2,n+1)
    plt.plot(history.epoch, history.history[metric], color=colors[0], label='Train')
    plt.plot(history.epoch, history.history['val_'+metric],
             color=colors[0], linestyle="--", label='Val')
    plt.xlabel('Epoch')
    plt.ylabel(name)
    if metric == 'loss':
      plt.ylim([0, plt.ylim()[1]])
    elif metric == 'auc':
      plt.ylim([0.8,1])
    else:
      plt.ylim([0,1])

    plt.legend()

plot_metrics(baseline_history)

"""## Evaluate metrics
You can use a confusion matrix to summarize the actual vs. predicted labels, where the X axis is the predicted label and the Y axis is the actual label:
"""

train_predictions_baseline = model.predict(train_features, batch_size=BATCH_SIZE)
test_predictions_baseline = model.predict(test_features, batch_size=BATCH_SIZE)

def plot_cm(labels, predictions, p=0.5):
  cm = confusion_matrix(labels, predictions > p)
  plt.figure(figsize=(5,5))
  sns.heatmap(cm, annot=True, fmt="d")
  plt.title('Confusion matrix @{:.2f}'.format(p))
  plt.ylabel('Actual label')
  plt.xlabel('Predicted label')

  print('Legitimate Transactions Detected (True Negatives): ', cm[0][0])
  print('Legitimate Transactions Incorrectly Detected (False Positives): ', cm[0][1])
  print('Fraudulent Transactions Missed (False Negatives): ', cm[1][0])
  print('Fraudulent Transactions Detected (True Positives): ', cm[1][1])
  print('Total Fraudulent Transactions: ', np.sum(cm[1]))

baseline_results = model.evaluate(test_features, test_labels,
                                  batch_size=BATCH_SIZE, verbose=0)
for name, value in zip(model.metrics_names, baseline_results):
  print(name, ': ', value)
print()

plot_cm(test_labels, test_predictions_baseline)

#test_labels
test_predictions_baseline

from sklearn.metrics import confusion_matrix
confusion_matrix_nn = confusion_matrix(test_labels, test_predictions_baseline >= 0.5)
print(confusion_matrix_nn)

conf_matrix_nn =pd.DataFrame(data=confusion_matrix_nn,columns=['Predicted as Unbanked:0','Predicted as Banked:1'],index=['Actually Unbanked:0','Actually Banked:1'])
plt.figure(figsize = (10,8))
plt.figure(figsize = (10,8))
sns.heatmap(conf_matrix_nn, annot=True,fmt='d',cmap="YlGnBu");

print(classification_report(test_labels, test_predictions_baseline >= 0.5))

perf_measure(test_labels, test_predictions_baseline >= 0.5)

Y_nn_score = (test_predictions_baseline >= 0.5)

nn_roc_auc = roc_auc_score(test_labels, test_predictions_baseline >= 0.5)
fpr, tpr, thresholds = roc_curve(test_labels, test_predictions_baseline)
plt.figure(figsize = (10,8))
plt.plot(fpr, tpr, label='TensorFlow Neural Network Model (area = %0.2f)' % nn_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic curve for TensorFlow Neural Network Model')
plt.legend(loc="lower right")
plt.savefig('NN_ROC')
plt.show()

"""## Plot the ROC
Now plot the ROC. This plot is useful because it shows, at a glance, the range of performance the model can reach just by tuning the output threshold.
"""

def plot_roc(name, labels, predictions, **kwargs):
  fp, tp, _ = sklearn.metrics.roc_curve(labels, predictions)

  plt.plot(100*fp, 100*tp, label=name, linewidth=2, **kwargs)
  plt.xlabel('False positives [%]')
  plt.ylabel('True positives [%]')
  plt.xlim([-0.5,100])
  plt.ylim([0,100.5])
  plt.grid(True)
  ax = plt.gca()
  ax.set_aspect('equal')

plot_roc("Train Baseline", train_labels, train_predictions_baseline, color=colors[0])
plot_roc("Test Baseline", test_labels, test_predictions_baseline, color=colors[3], linestyle='--')
plt.legend(loc='lower right')

def plot_prc(name, labels, predictions, **kwargs):
    precision, recall, _ = sklearn.metrics.precision_recall_curve(labels, predictions)

    plt.plot(precision, recall, label=name, linewidth=2, **kwargs)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.grid(True)
    ax = plt.gca()
    ax.set_aspect('equal')

plot_prc("Train Baseline", train_labels, train_predictions_baseline, color=colors[0])
plot_prc("Test Baseline", test_labels, test_predictions_baseline, color=colors[0], linestyle='--')
plt.legend(loc='lower right')

"""### ***************************************** End ********************************************* ###"""

