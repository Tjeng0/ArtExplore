from PIL import Image
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from skimage.color import lab2rgb,rgb2lab
import operator
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
np.set_printoptions(threshold=sys.maxsize)
matplotlib.use('TKAgg', warn=False, force=True)

def convertImageToArray(filename, size):
    im = Image.open(filename)
    size = size, size
    im.thumbnail(size, Image.ANTIALIAS)
    array = np.array(im.getdata())
    return rgbtolab(array)

def rgbtolab(arr):
    res = arr.copy()/255
    res = res.reshape([1, arr.shape[0], 3])
    res = rgb2lab(res)
    res = res.reshape([arr.shape[0], 3])
    return res

def labtorgb(arr):
    res = arr.copy()
    res = res.reshape([1, arr.shape[0], 3])
    res = lab2rgb(res)
    res = res.reshape([arr.shape[0], 3])
    return res

def kmeans(data, k):
    km = KMeans(k, n_init = 10).fit(data)
    return km.cluster_centers_, km.labels_

def getDistributionFrame(centers, labels):
    counts = np.unique(labels, return_counts=True)[1]
    distribution = counts / np.sum(counts)
    centers = labtorgb(centers)
    frame = pd.DataFrame(centers, columns=['r','g','b'])
    frame['p'] = distribution
    return frame

def colorPie(kf):
    plt.pie(kf['p'], colors=(kf.loc[:,'r':'b']).to_numpy())
    plt.show()

def analyzeImage(filename, size):
    df = convertImageToArray(filename, size)
    clusterdict = {}
    silhouettedict = {}
    for i in range(3, 10):
        centers, labels = kmeans(df, i)
        clusterdict[i] = {'centers': centers, 'labels': labels}
        silhouettedict[i] = silhouette_score(df, labels, sample_size = 4000)
        print("Silhouette score with k=" + str(i) + " is " + str(silhouettedict[i]))
    maxsilhouette = clusterdict[max(silhouettedict.items(), key= lambda k: k[1])[0]]
    result = getDistributionFrame(maxsilhouette['centers'], maxsilhouette['labels'])
    return result

def groupTest(filename):
    groupList = []
    for size in range(50, 350, 50):
        groupList.append(analyzeImage(filename, size))
    for df in groupList:
        df = (df.sort_values(by=['p'])*255).round(1).reset_index(drop=True)
        print(df)

groupTest('../../assets/girl-earring.jpg')
