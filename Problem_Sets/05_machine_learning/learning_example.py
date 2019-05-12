"""
Implements the learning process specified in Problem Set 5, for illustrative purposes for myself.

Author: Mark Xavier
"""

import sys
import math

MAXINT = 200000000

class Classifier(object):
    """
    """

    def __init__(self, training_set, num_categories):
        """
        """

        self.training_set = training_set
        self.num_categories = num_categories

    def learn(self):
        """
        """

        self.centroids = [None for i in range(self.num_categories)]
        denominators = [0.0 for i in range(self.num_categories)]
        for row in self.training_set:
            category = row[3]
            if self.centroids[category] == None:
                self.centroids[category] = row[:3]
            else:
                self.centroids[category] = [self.centroids[category][i] + row[i] for i in range(3)]
            denominators[category] += 1.0

        for index, centroid in enumerate(self.centroids):
            self.centroids[index] = [self.centroids[index][j] / denominators[index] for j in range(3)]

    def classify(self, instance):
        """
        """

        min_distance = MAXINT
        centroid_index = None
        for i, centroid in enumerate(self.centroids):
            current_distance = 0
            for index, value in enumerate(centroid):
                current_distance += (instance[index] - value)**2

            if current_distance < min_distance:
                min_distance = current_distance
                centroid_index = i

        return centroid_index

def test_classifier(training_set=None):
    """
    """

    if training_set == None:
        training_set = [
                        [1, 1, 2, 0],
                        [2, 1, 1, 0],
                        [2, 0, 1, 0],
                        [0, 2, 1, 1],
                        [3, 2, 0, 1],
                        [3, 3, 0, 2],
                        [0, 3, 0, 2],
                        [3, 2, 1, 2],
                        [0, 3, 3, 2]
                       ]

    classifier = Classifier(training_set, 3)
    classifier.learn()
    accuracy = 0
    for row in training_set:
        x = classifier.classify(row[:3])
        print("<%.2f, %.2f, %.2f> classified as %d, labled %d" % (row[0], row[1], row[2], x, row[3]))
        if x == row[3]:
            accuracy += 1

    n = len(training_set)
    perc = accuracy / float(n)
    print("\nAccuracy = %d / %d (%.2f)" % (accuracy, n, perc))

if __name__ == '__main__':
    test_classifier()
