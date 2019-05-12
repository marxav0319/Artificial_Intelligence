import numpy as np

def calc_distance(vec, other):
    """
    """

    distance = 0
    for i in range(len(vec[:3])):
        distance += ((vec[i] - other[i]) ** 2)

    return np.sqrt(distance)

def get_max(results):
    """
    """

    ind = -1
    maxim = -1
    for i in range(len(results)):
        if results[i][1] > maxim:
            maxim = results[i][1]
            ind = i
    return ind

def k_nearest_neighbors(num, train, pred):
    """
    """

    results = []
    for index, vector in enumerate(train):
        distance = calc_distance(vector, pred)
        if len(results) < num:
            results.append([index, distance])
        else:
            max_ind = get_max(results)
            if results[max_ind][1] > distance:
                results[max_ind] = [index, distance]

    return results

def test():
    """
    """

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

    pred = [2, 2, 2]

    results = k_nearest_neighbors(3, training_set, pred)
    for res in results:
        print(training_set[res[0]])

if __name__ == '__main__':
    test()
