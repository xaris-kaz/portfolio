#Kazakidis Theocharis
#4679
#Kazakidis Konstantinos
#4065


import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def accuracy(tp,tn,pos,neg):
    return (tp+tn)/(pos+neg)

def precision(tp,fp):
    return tp/(tp+fp)

def recall(tp,fn):
    return tp/(tp+fn)

def f1score(precision,recall):
    return 2*(precision*recall)/(precision+recall)


train_set=pd.read_csv('train.csv')#gia ta apotelesmata sto notebook valame tin entoli train_set=pd.read_csv('../input/ghouls-ghost-goblin/train.csv')
print(train_set)


monster_color = {'white':0,'black':1,'clear':2,'blue':3,'green':4,'blood':5}
monster_type = {'Ghost':0, 'Goblin':1,'Ghoul':2}

train_set.replace({'color':monster_color,'type':monster_type},inplace=True)
print(train_set)

x = train_set.loc[:, 'bone_length':'color'].values
y = train_set.loc[:, 'type'].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, stratify=y)


#KNN

K= [1, 3, 5, 10]

for k in K:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train,y_train)
    y_pred = knn.predict(x_test)
    cm = confusion_matrix(y_test,y_pred)
  
    tp_ghost = cm[0][0]
    fn_ghost = cm[0][1]+cm[0][2]
    fp_ghost = cm[1][0] +cm[2][0]
    tn_ghost = cm[1][1]+cm[1][2] +cm[1][0]+cm[2][1]+cm[2][2]
    ghost_positive = tp_ghost+ fn_ghost
    ghost_negative = fp_ghost + tn_ghost 
    ghost_accuracy = accuracy(tp_ghost,tn_ghost,ghost_positive,ghost_negative)
    ghost_precision = precision(tp_ghost,fp_ghost)
    ghost_recall =recall(tp_ghost,fn_ghost)
    ghost_f1score = f1score(ghost_precision,ghost_recall)
    print(f" Ghost \n k: {k}  \n Accuracy: {ghost_accuracy} \n Precision:{ghost_precision} \n Recall: {ghost_recall} \n F1 score: {ghost_f1score} \n")
    
    tp_goblin = cm[1][1]
    fn_goblin = cm[1][0] +cm[1][2]
    fp_goblin = cm[0][1] +cm[2][1]
    tn_goblin = cm[0][0]+cm[0][2]+cm[2][0]+cm[2][2]
    goblin_positive = tp_goblin+fn_goblin
    goblin_negative =fp_goblin+ tn_goblin
    goblin_accuracy = accuracy(tp_goblin,tn_goblin,goblin_positive,goblin_negative)
    goblin_precision = precision(tp_goblin,fp_goblin)
    goblin_recall =recall(tp_goblin,fn_goblin)
    goblin_f1score = f1score(goblin_precision,goblin_recall)
    print(f" Goblin \n k: {k}  \n Accuracy: {goblin_accuracy} \n Precision:{goblin_precision} \n Recall: {goblin_recall} \n F1 score: {goblin_f1score} \n")
        
    tp_ghoul = cm[2][2]
    fn_ghoul = cm[2][0]+cm[2][1]
    fp_ghoul= cm[0][2]+cm[1][2]
    tn_ghoul = cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]
    ghoul_positive = tp_ghoul+fn_ghoul
    ghoul_negative =fp_ghoul+ tn_ghoul
    ghoul_accuracy = accuracy(tp_ghoul,tn_ghoul,ghoul_positive,ghoul_negative)
    ghoul_precision = precision(tp_ghoul,fp_ghoul)
    ghoul_recall =recall(tp_ghoul,fn_ghoul)
    ghoul_f1score = f1score(ghoul_precision,ghoul_recall)
    print(f" Ghoul \n k: {k}  \n Accuracy: {ghoul_accuracy} \n Precision:{ghoul_precision} \n Recall: {ghoul_recall} \n F1 score: {ghoul_f1score} \n")
    
    total_tp = tp_ghost+ tp_goblin +tp_ghoul
    total_fn = fn_ghost+fn_goblin+fn_ghoul 
    total_fp = fp_ghost + fp_goblin + fp_ghoul
    total_tn =tn_ghost+ tn_goblin+tn_ghoul
    total_positive = total_tp+total_fn
    total_negative =total_fp+ total_tn
    total_accuracy = accuracy(total_tp,total_tn,total_positive,total_negative)
    total_precision = precision(total_tp,total_fp)
    total_recall =recall(total_tp,total_fn)
    total_f1score = f1score(total_precision,total_recall)
    print(f" Total \n k: {k}  \n Accuracy: {total_accuracy} \n Precision:{total_precision} \n Recall: {total_recall} \n F1 score: {total_f1score} \n")


#Neural Network

hidden_layers = [
    (50,),(100,),(200,),
    (50,25,),(100,50,),(200,100,)
]

for hl in hidden_layers:
    clf = MLPClassifier(hidden_layer_sizes=hl,activation='tanh',solver='sgd',max_iter=200,random_state=1).fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    cm = confusion_matrix(y_test,y_pred)
    
    tp_ghost = cm[0][0]
    fn_ghost = cm[0][1]+cm[0][2]
    fp_ghost = cm[1][0] +cm[2][0]
    tn_ghost = cm[1][1]+cm[1][2] +cm[1][0]+cm[2][1]+cm[2][2]
    ghost_positive = tp_ghost+ fn_ghost
    ghost_negative = fp_ghost + tn_ghost 
    ghost_accuracy = accuracy(tp_ghost,tn_ghost,ghost_positive,ghost_negative)
    ghost_precision = precision(tp_ghost,fp_ghost)
    ghost_recall =recall(tp_ghost,fn_ghost)
    ghost_f1score = f1score(ghost_precision,ghost_recall)
    print(f" Ghost \n Hidden layers: {hl}  \n Accuracy: {ghost_accuracy} \n Precision:{ghost_precision} \n Recall: {ghost_recall} \n F1 score: {ghost_f1score} \n")
    
    tp_goblin = cm[1][1]
    fn_goblin = cm[1][0] +cm[1][2]
    fp_goblin = cm[0][1] +cm[2][1]
    tn_goblin = cm[0][0]+cm[0][2]+cm[2][0]+cm[2][2]
    goblin_positive = tp_goblin+fn_goblin
    goblin_negative =fp_goblin+ tn_goblin
    goblin_accuracy = accuracy(tp_goblin,tn_goblin,goblin_positive,goblin_negative)
    goblin_precision = precision(tp_goblin,fp_goblin)
    goblin_recall =recall(tp_goblin,fn_goblin)
    goblin_f1score = f1score(goblin_precision,goblin_recall)
    print(f" Goblin \n Hidden layers: {hl}  \n Accuracy: {goblin_accuracy} \n Precision:{goblin_precision} \n Recall: {goblin_recall} \n F1 score: {goblin_f1score} \n")
        
    tp_ghoul = cm[2][2]
    fn_ghoul = cm[2][0]+cm[2][1]
    fp_ghoul= cm[0][2]+cm[1][2]
    tn_ghoul = cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]
    ghoul_positive = tp_ghoul+fn_ghoul
    ghoul_negative =fp_ghoul+ tn_ghoul
    ghoul_accuracy = accuracy(tp_ghoul,tn_ghoul,ghoul_positive,ghoul_negative)
    ghoul_precision = precision(tp_ghoul,fp_ghoul)
    ghoul_recall =recall(tp_ghoul,fn_ghoul)
    ghoul_f1score = f1score(ghoul_precision,ghoul_recall)
    print(f" Ghoul \n Hidden layers: {hl}  \n Accuracy: {ghoul_accuracy} \n Precision:{ghoul_precision} \n Recall: {ghoul_recall} \n F1 score: {ghoul_f1score} \n")
    
    
    total_tp = tp_ghost+ tp_goblin +tp_ghoul
    total_fn = fn_ghost+fn_goblin+fn_ghoul 
    total_fp = fp_ghost + fp_goblin + fp_ghoul
    total_tn =tn_ghost+ tn_goblin+tn_ghoul
    total_positive = total_tp+total_fn
    total_negative =total_fp+ total_tn
    total_accuracy = accuracy(total_tp,total_tn,total_positive,total_negative)
    total_precision = precision(total_tp,total_fp)
    total_recall =recall(total_tp,total_fn)
    total_f1score = f1score(total_precision,total_recall)
    print(f" Total \n Hidden layers: {hl}  \n Accuracy: {total_accuracy} \n Precision:{total_precision} \n Recall: {total_recall} \n F1 score: {total_f1score} \n")


#SVM

kernels =['linear','rbf']


for k in kernels:
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto',kernel=k))
    clf.fit(x_train, y_train)
    y_pred =clf.predict(x_test)
    cm = confusion_matrix(y_test,y_pred)
    
    tp_ghost = cm[0][0]
    fn_ghost = cm[0][1]+cm[0][2]
    fp_ghost = cm[1][0] +cm[2][0]
    tn_ghost = cm[1][1]+cm[1][2] +cm[1][0]+cm[2][1]+cm[2][2]
    ghost_positive = tp_ghost+ fn_ghost
    ghost_negative = fp_ghost + tn_ghost 
    ghost_accuracy = accuracy(tp_ghost,tn_ghost,ghost_positive,ghost_negative)
    ghost_precision = precision(tp_ghost,fp_ghost)
    ghost_recall =recall(tp_ghost,fn_ghost)
    ghost_f1score = f1score(ghost_precision,ghost_recall)
    print(f" Ghost \n Kernel: {k}  \n Accuracy: {ghost_accuracy} \n Precision:{ghost_precision} \n Recall: {ghost_recall} \n F1 score: {ghost_f1score} \n")
    
    tp_goblin = cm[1][1]
    fn_goblin = cm[1][0] +cm[1][2]
    fp_goblin = cm[0][1] +cm[2][1]
    tn_goblin = cm[0][0]+cm[0][2]+cm[2][0]+cm[2][2]
    goblin_positive = tp_goblin+fn_goblin
    goblin_negative =fp_goblin+ tn_goblin
    goblin_accuracy = accuracy(tp_goblin,tn_goblin,goblin_positive,goblin_negative)
    goblin_precision = precision(tp_goblin,fp_goblin)
    goblin_recall =recall(tp_goblin,fn_goblin)
    goblin_f1score = f1score(goblin_precision,goblin_recall)
    print(f" Goblin \n Kernel: {k}  \n Accuracy: {goblin_accuracy} \n Precision:{goblin_precision} \n Recall: {goblin_recall} \n F1 score: {goblin_f1score} \n")
        
    tp_ghoul = cm[2][2]
    fn_ghoul = cm[2][0]+cm[2][1]
    fp_ghoul= cm[0][2]+cm[1][2]
    tn_ghoul = cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]
    ghoul_positive = tp_ghoul+fn_ghoul
    ghoul_negative =fp_ghoul+ tn_ghoul
    ghoul_accuracy = accuracy(tp_ghoul,tn_ghoul,ghoul_positive,ghoul_negative)
    ghoul_precision = precision(tp_ghoul,fp_ghoul)
    ghoul_recall =recall(tp_ghoul,fn_ghoul)
    ghoul_f1score = f1score(ghoul_precision,ghoul_recall)
    print(f" Ghoul \n Kernel: {k}  \n Accuracy: {ghoul_accuracy} \n Precision:{ghoul_precision} \n Recall: {ghoul_recall} \n F1 score: {ghoul_f1score} \n")
    
    
    total_tp = tp_ghost+ tp_goblin +tp_ghoul
    total_fn = fn_ghost+fn_goblin+fn_ghoul 
    total_fp = fp_ghost + fp_goblin + fp_ghoul
    total_tn =tn_ghost+ tn_goblin+tn_ghoul
    total_positive = total_tp+total_fn
    total_negative =total_fp+ total_tn
    total_accuracy = accuracy(total_tp,total_tn,total_positive,total_negative)
    total_precision = precision(total_tp,total_fp)
    total_recall =recall(total_tp,total_fn)
    total_f1score = f1score(total_precision,total_recall)
    print(f" Total \n Kernel: {k}  \n Accuracy: {total_accuracy} \n Precision:{total_precision} \n Recall: {total_recall} \n F1 score: {total_f1score} \n")

    


#Naive Bayes

gauss_clf = GaussianNB()
multi_clf = MultinomialNB()

gauss_clf.fit(x_train[:,0:3], y_train)
gauss_proba =gauss_clf.predict_proba(x_test[:,0:3])

multi_clf.fit(x_train[:,4].reshape(-1,1), y_train)
multi_proba =multi_clf.predict_proba(x_test[:,4].reshape(-1,1))

finals = np.multiply(gauss_proba, multi_proba)
normalised = finals.T/(np.sum(finals, axis=1) + 1e-6)#gia suntomia 1e-6=0.000001
normalised = np.moveaxis(normalised, [0, 1], [1, 0])

y_pred = np.argmax(normalised, axis=1)

cm = confusion_matrix(y_test,y_pred)
    
tp_ghost = cm[0][0]
fn_ghost = cm[0][1]+cm[0][2]
fp_ghost = cm[1][0] +cm[2][0]
tn_ghost = cm[1][1]+cm[1][2] +cm[1][0]+cm[2][1]+cm[2][2]
ghost_positive = tp_ghost+ fn_ghost
ghost_negative = fp_ghost + tn_ghost 
ghost_accuracy = accuracy(tp_ghost,tn_ghost,ghost_positive,ghost_negative)
ghost_precision = precision(tp_ghost,fp_ghost)
ghost_recall =recall(tp_ghost,fn_ghost)
ghost_f1score = f1score(ghost_precision,ghost_recall)
print(f" Ghost \n Accuracy: {ghost_accuracy} \n Precision:{ghost_precision} \n Recall: {ghost_recall} \n F1 score: {ghost_f1score} \n")
    
tp_goblin = cm[1][1]
fn_goblin = cm[1][0] +cm[1][2]
fp_goblin = cm[0][1] +cm[2][1]
tn_goblin = cm[0][0]+cm[0][2]+cm[2][0]+cm[2][2]
goblin_positive = tp_goblin+fn_goblin
goblin_negative =fp_goblin+ tn_goblin
goblin_accuracy = accuracy(tp_goblin,tn_goblin,goblin_positive,goblin_negative)
goblin_precision = precision(tp_goblin,fp_goblin)
goblin_recall =recall(tp_goblin,fn_goblin)
goblin_f1score = f1score(goblin_precision,goblin_recall)
print(f" Goblin \n Accuracy: {goblin_accuracy} \n Precision:{goblin_precision} \n Recall: {goblin_recall} \n F1 score: {goblin_f1score} \n")
        
tp_ghoul = cm[2][2]
fn_ghoul = cm[2][0]+cm[2][1]
fp_ghoul= cm[0][2]+cm[1][2]
tn_ghoul = cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]
ghoul_positive = tp_ghoul+fn_ghoul
ghoul_negative =fp_ghoul+ tn_ghoul
ghoul_accuracy = accuracy(tp_ghoul,tn_ghoul,ghoul_positive,ghoul_negative)
ghoul_precision = precision(tp_ghoul,fp_ghoul)
ghoul_recall =recall(tp_ghoul,fn_ghoul)
ghoul_f1score = f1score(ghoul_precision,ghoul_recall)
print(f" Ghoul \n MultinomialNB  \n Accuracy: {ghoul_accuracy} \n Precision:{ghoul_precision} \n Recall: {ghoul_recall} \n F1 score: {ghoul_f1score} \n")
    
    
total_tp = tp_ghost+ tp_goblin +tp_ghoul
total_fn = fn_ghost+fn_goblin+fn_ghoul 
total_fp = fp_ghost + fp_goblin + fp_ghoul
total_tn =tn_ghost+ tn_goblin+tn_ghoul
total_positive = total_tp+total_fn
total_negative =total_fp+ total_tn
total_accuracy = accuracy(total_tp,total_tn,total_positive,total_negative)
total_precision = precision(total_tp,total_fp)
total_recall =recall(total_tp,total_fn)
total_f1score = f1score(total_precision,total_recall)
print(f" Total \n Accuracy: {total_accuracy} \n Precision:{total_precision} \n Recall: {total_recall} \n F1 score: {total_f1score} \n")







