"""
Author: Pranav Srivastava
Detail: Distance Weighted KNN Regression
"""

import numpy as np
import sys

class DistanceWeightedKNNRegression:

    def __init__(self, k, trainingdataset, testdataset):
        self.k = k
        self.num_of_features = 12
        self.trainingdataset = trainingdataset
        self.testdataset = testdataset
        self.accurate_predictions = 0
        self.predicted_regressions = np.empty(shape=[0])
        self.actual_regression  = np.empty(shape=[0])
        self.accuracy = 0

    def calculateDistances(self,training_data, test_instance):

        result = np.empty(shape=[0,0])
        ind = np.empty(shape=[0])

        #slice numpy array to leave the class columnn
        training_data = training_data[:,:-1]
        test_instance = test_instance[:-1]
        
        #reshaping the single query instance into 2d numpy so that it can be computed for eucledian distance
        test_instance = np.reshape(test_instance, (1, self.num_of_features))

        result = np.sqrt(-2 * np.dot(test_instance, training_data.T) + np.sum(training_data**2,    axis=1) + np.sum(test_instance**2, axis=1)[:, np.newaxis])
        
        ind = np.argsort(result, axis=1) # sorts along last axis (across)
        return result, ind

    def predictRegression(self, distances, testdata_regression):

        w = (np.sum(np.square(np.reciprocal(distances))))
        wfx = np.sum(np.multiply(testdata_regression,np.square(np.reciprocal(distances))))
        fx = wfx/w

        return fx

    def predictkNNClass(self):
        training_data = self.trainingdataset
        test_instance = self.testdataset
        
        result = np.empty(shape=[0,0])
        distances = np.empty(shape=[0,0])
        ind = np.empty(shape=[0])    

        class_vector_training = training_data[:,self.num_of_features]
        class_vector_test = test_instance[:,self.num_of_features]

        knnResult = []

        test_data_size = test_instance.shape[0]

        for i in range(0, test_data_size):

            result = []

            result = self.calculateDistances(training_data, test_instance[i])
            
            distances = result[0]
            ind = result[1]
            
            k_near_distances = (np.take(distances, ind))[:,0:self.k]
            training_vector = (np.take(class_vector_training, ind))[:,0:self.k]

            regressionValue = self.predictRegression(k_near_distances, training_vector)
            print(k_near_distances,training_vector)
            print("regressionValue>>",regressionValue)

            knnResult.append(regressionValue)

            #if voteDW == class_vector_test[i]:
            #    self.accurate_predictions +=1
        self.predicted_regressions = np.array(knnResult)
        self.actual_regression = class_vector_test
        print("class vector test>>",class_vector_test)
        
        print("R2 metric is: ", self.r2metric())



    def r2metric(self):
        # This method calcuates the r2 metri.
        pregressions = np.reshape(self.predicted_regressions, (1, self.predicted_regressions.shape[0]))
        actualreg = np.reshape(self.actual_regression, (1, self.actual_regression.shape[0]))
        avg = np.average(actualreg)

        sumofsquaredresiduals = -2 * np.dot(pregressions, actualreg.T) + np.sum(actualreg**2,    axis=1) + np.sum(pregressions**2, axis=1)[:, np.newaxis]
        #print("sum of residuals: ",sumofsquaredresiduals[0][0])

        totalsumofsquares = np.sum(np.square(actualreg - avg))

        #print("total sum of squares", totalsumofsquares)
        rsquare = 1-(sumofsquaredresiduals[0][0]/totalsumofsquares)
        #assign accuracy value
        self.accuracy = rsquare
        print("accuracy percentage: ",rsquare*100)
        return rsquare


testdataset = np.genfromtxt('data/regression/testData.csv', delimiter=',')
trainingdataset = np.genfromtxt('data/regression/trainingData.csv', delimiter=',')

#trainingdataset = np.genfromtxt('trainingset.csv', delimiter=',')
#testdataset = np.genfromtxt('test.csv', delimiter=',')

k = int(sys.argv[1])
filename = sys.argv[2]
remark = sys.argv[3]


dwknnr = DistanceWeightedKNNRegression(k, trainingdataset, testdataset)

dwknnr.predictkNNClass()

results = []
results.append(dwknnr.k)
results.append(dwknnr.accuracy)
results.append(filename)
results.append(remark)

with open('test_results.txt', 'a') as f:
    f.write((str("%s\n" % results)))