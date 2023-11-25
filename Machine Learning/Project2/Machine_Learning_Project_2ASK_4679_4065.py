#Kazakidis Theocharis
#4679
#Kazakidis Konstantinos
#4065

# In[1]:


import os
import glob
import random
import fnmatch
import numpy as np
from PIL import Image
np.random.seed(0)


# In[2]:


train_data_path = os.path.join('11785-spring2021-hw2p2s1-face-classification','train_data')


# In[3]:


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

class CustomDatset:
    def __init__(self,imgs_path,K):
        self.data = []
        classes=[]
        for class_path in os.listdir(imgs_path):
            count = len(fnmatch.filter(glob.glob(os.path.join(imgs_path,class_path,"*.jpg")), "*.jpg"))
            if count >=50:
                classes.append(class_path)
        self.selected_classes = random.sample(classes,K)
        for class_name in self.selected_classes:
            for img_path in glob.glob(os.path.join(imgs_path,class_name,"*.jpg"))[:50]:
                self.data.append([img_path, class_name])

    def __len__(self):
        return len(self.data)

    @property
    def get_data(self):
        images=[]
        labels =[]
        for image,label in self.data:
            gray = rgb2gray(np.array(Image.open(image)))
            images.append(gray)
            labels.append(label)
        return np.array(images).astype(np.float32),np.array(labels,dtype=np.int32)


# In[4]:


data_set = CustomDatset(train_data_path,10)
images,labels = data_set.get_data
classes = data_set.selected_classes


# In[5]:


train_nsamples, train_nx, train_ny = images.shape
train_images2d = images.reshape((train_nsamples,train_nx*train_ny))

y_train = np.array(labels,dtype=np.int32)

from sklearn.decomposition import PCA

class DecreasedDimesions:
    def __init__(self,dimesion,pc_train):
        self.dimesion = dimesion
        self.pc_train = pc_train

decreased_data=[]
for M in [100,50,25]:
    pca = PCA(n_components=M)
    pc_train = pca.fit_transform(train_images2d)
    pc_train_scores = pca.transform(train_images2d)
    d = DecreasedDimesions(M,pc_train_scores)
    decreased_data.append(d)


# In[6]:


def euclidean_distances(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


def cosine_distances(x1,x2):
    return 1 - (np.sum(x1*x2)/np.sqrt(np.sum(x1**2)) * np.sqrt(np. sum(x2**2)))

class KMeans:

    def __init__(self, K=10, distance ='euclidean',max_iters=300, plot_steps=False):
        self.K = K
        self.distance = distance
        self.max_iters = max_iters
        self.plot_steps = plot_steps
        self.clusters = [[] for _ in range(self.K)]
        self.centroids = []

    def predict(self, X):
        self.X = X
        self.n_samples, self.n_features = X.shape


        random_sample_idxs = np.random.choice(self.n_samples, self.K, replace=False)
        self.centroids = [self.X[idx] for idx in random_sample_idxs]


        for _ in range(self.max_iters):

            self.clusters = self._create_clusters(self.centroids)

            if self.plot_steps:
                self.plot()


            centroids_old = self.centroids
            self.centroids = self._get_centroids(self.clusters)

            if self._is_converged(centroids_old, self.centroids):
                break

            if self.plot_steps:
                self.plot()


        return self._get_cluster_labels(self.clusters)


    def _get_cluster_labels(self, clusters):

        labels = np.empty(self.n_samples)

        for cluster_idx, cluster in enumerate(clusters):
            for sample_index in cluster:
                labels[sample_index] = cluster_idx
        return labels

    def _create_clusters(self, centroids):
        clusters = [[] for _ in range(self.K)]
        for idx, sample in enumerate(self.X):
            centroid_idx = self._closest_centroid(sample, centroids)
            clusters[centroid_idx].append(idx)
        return clusters

    def _closest_centroid(self, sample, centroids):
        distances =[]
        if self.distance =='euclidean':
            for point in centroids:
                distances.append(euclidean_distances(sample,point))
        else:
            for point in centroids:
                distances.append(cosine_distances(sample,point))
        closest_index = np.argmin(distances)
        return closest_index

    def _get_centroids(self, clusters):
        centroids = np.zeros((self.K, self.n_features))
        for cluster_idx, cluster in enumerate(clusters):
            cluster_mean = np.mean(self.X[cluster], axis=0)
            centroids[cluster_idx] = cluster_mean
        return centroids

    def _is_converged(self, centroids_old, centroids):
        distances =[]
        if self.distance =='euclidean':
            for i in range(self.K):
                distances.append(euclidean_distances(centroids_old[i], centroids[i]))
        else:
            for i in range(self.K):
                distances.append(cosine_distances(centroids_old[i], centroids[i]))
        return sum(distances) == 0


# In[9]:


from sklearn.metrics import confusion_matrix,f1_score
from sklearn.cluster import AgglomerativeClustering


def purity_score(y_test, y_pred):
    cm = confusion_matrix(y_test,y_pred)
    return np.sum(np.amax(cm, axis=0)) / np.sum(cm)


for M in [100,50,25]:
    print('-'*100)
    print(M)
    print('-'*100)
    pc_train = next(d.pc_train for d in decreased_data if d.dimesion == M)
    agglomerative = AgglomerativeClustering(n_clusters=10, affinity='euclidean', linkage='ward').fit_predict(pc_train)
    for distance in ['euclidean','cosine']:
        kmeans = KMeans(distance=distance).predict(pc_train)
        total_f1score_kmeans = np.sum(f1_score(labels,kmeans,average=None))
        print(f'Total Fscore Kmeans -> {total_f1score_kmeans}')
        print(f'Purity KMeans: {M} {distance} -> {purity_score(labels,kmeans)}')

    print(f'Purity AgglomerativeClustering{M} -> {purity_score(labels,agglomerative)}')
    total_f1score_agglomerative_clustering = np.sum(f1_score(labels,agglomerative,average=None))
    print(f'Total Fscore AgglomerativeClustering -> {total_f1score_agglomerative_clustering}')


# In[ ]:




