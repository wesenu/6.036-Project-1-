from string import punctuation, digits

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import copy

### Part I

def hinge_loss(feature_matrix, labels, theta, theta_0):
    """
    Section 1.2
    Finds the total hinge loss on a set of data given specific classification
    parameters.

    Args:
        feature_matrix - A numpy matrix describing the given data. Each row
            represents a single data point.
        labels - A numpy array where the kth element of the array is the
            correct classification of the kth row of the feature matrix.
        theta - A numpy array describing the linear classifier.
        theta_0 - A real valued number representing the offset parameter.


    Returns: A real number representing the hinge loss associated with the
    given dataset and parameters. This number should be the average hinge
    loss across all of the points in the feature matrix.
    """
    total_hinge_loss = 0

    for i in range(len(feature_matrix)): 
        value = labels[i]*(np.dot(theta, feature_matrix[i]) +theta_0)
        if  value  <= 1:
            hinge_loss = 1 - value
        else:
            hinge_loss = 0
        total_hinge_loss += hinge_loss
    return total_hinge_loss/len(feature_matrix)



    # raise NotImplementedError


print ("this is being imported and run")

def perceptron_single_step_update(feature_vector, label, current_theta, current_theta_0):
    """
    Section 1.3
    Properly updates the classification parameter, theta and theta_0, on a
    single step of the perceptron algorithm.

    Args:
        feature_vector - A numpy array describing a single data point.
        label - The correct classification of the feature vector.
        current_theta - The current theta being used by the perceptron
            algorithm before this update.
        current_theta_0 - The current theta_0 being used by the perceptron
            algorithm before this update.

    Returns: A tuple where the first element is a numpy array with the value of
    theta after the current update has completed and the second element is a
    real valued number with the value of theta_0 after the current updated has
    completed.
    """
    # raise NotImplementedError
    # normalized_feature_vector = normalize_vector(featu    re_vector)
    value = label*(np.dot(current_theta,feature_vector) + current_theta_0)
    # print (type(current_theta), type(feature_vector), type(current_theta_0))
    # print (type(value), "PRINTING")
    if value <=0:
        next_theta = current_theta + label*feature_vector
        next_theta_0 = current_theta_0 + label
        return (next_theta, next_theta_0)

    return (current_theta, current_theta_0)



    

def perceptron(feature_matrix, labels, T):
    """
    Section 1.4a
    Runs the full perceptron algorithm on a given set of data. Runs T
    iterations through the data set, there is no need to worry about
    stopping early.

    NOTE: Please use the previously implemented functions when applicable.
    Do not copy paste code from previous parts.

    Args:
        feature_matrix -  A numpy matrix describing the given data. Each row
            represents a single data point.
        labels - A numpy array where the kth element of the array is the
            correct classification of the kth row of the feature matrix.
        T - An integer indicating how many times the perceptron algorithm
            should iterate through the feature matrix.

    Returns: A tuple where the first element is a numpy array with the value of
    theta, the linear classification parameter, after T iterations through the
    feature matrix and the second element is a real number with the value of
    theta_0, the offset classification parameter, after T iterations through
    the feature matrix.
    """
    # raise NotImplementedError
    current_theta = np.zeros(np.shape(feature_matrix)[1])
    current_theta_0 = 0

    for i in range(T):
        for j in range(np.shape(feature_matrix)[0]):
            current_theta, current_theta_0 = perceptron_single_step_update(feature_matrix[j], labels[j],current_theta,current_theta_0)

    return (current_theta, current_theta_0) 




    
def average_perceptron(feature_matrix, labels, T):
    """
    Section 1.4b
    Runs the average perceptron algorithm on a given set of data. Runs T
    iterations through the data set, there is no need to worry about
    stopping early.

    NOTE: Please use the previously implemented functions when applicable.
    Do not copy paste code from previous parts.

    Args:
        feature_matrix -  A numpy matrix describing the given data. Each row
            represents a single data point.
        labels - A numpy array where the kth element of the array is the
            correct classification of the kth row of the feature matrix.
        T - An integer indicating how many times the perceptron algorithm
            should iterate through the feature matrix.

    Returns: A tuple where the first element is a numpy array with the value of
    the average theta, the linear classification parameter, found after T
    iterations through the feature matrix and the second element is a real
    number with the value of the average theta_0, the offset classification
    parameter, found after T iterations through the feature matrix.

    Hint: It is difficult to keep a running average; however, it is simple to
    find a sum and divide.
    """
    # raise NotImplementedError

    

    current_theta = np.zeros(np.shape(feature_matrix)[1])
    current_theta_0 = 0
    sum_theta, sum_theta_0 = np.zeros(np.shape(feature_matrix)[1]), 0

    for i in range(T):
        for j in range(len(feature_matrix)):
            update_theta = perceptron_single_step_update(feature_matrix[j], labels[j],current_theta,current_theta_0)
            current_theta, current_theta_0 = update_theta
            sum_theta = np.add(sum_theta, current_theta) 
            sum_theta_0 += current_theta_0
    return sum_theta/(len(feature_matrix)*T), sum_theta_0/(len(feature_matrix)*T)


    # return (current_theta, update_theta) 


def pegasos_single_step_update(feature_vector, label, L, eta, current_theta, current_theta_0):
    """
    Section 1.5
    Properly updates the classification parameter, theta and theta_0, on a
    single step of the Pegasos algorithm

    Args:
        feature_vector - A numpy array describing a single data point.
        label - The correct classification of the feature vector.
        L - The lamba value being used to update the parameters.
        eta - Learning rate to update parameters.
        current_theta - The current theta being used by the Pegasos
            algorithm before this update.
        current_theta_0 - The current theta_0 being used by the
            Pegasos algorithm before this update.

    Returns: A tuple where the first element is a numpy array with the value of
    theta after the current update has completed and the second element is a
    real valued number with the value of theta_0 after the current updated has
    completed.
    """
    

    value = label*(np.dot(current_theta,feature_vector) + current_theta_0)
    if value <= 1:
        next_theta = (1-L*eta)*current_theta + np.dot(eta*label, feature_vector)
        next_theta_0 = (1-L*eta)*current_theta_0 + eta*label
       

    else: 
        next_theta = (1-L*eta)*current_theta
        next_theta_0 = (1-L*eta)*current_theta_0
    return (next_theta, next_theta_0)


def pegasos(feature_matrix, labels, T, L):
    """
    Section 1.6
    Runs the Pegasos algorithm on a given set of data. Runs T
    iterations through the data set, there is no need to worry about
    stopping early.
    
    For each update, set learning rate = 1/sqrt(t), 
    where t is a counter for the number of updates performed so far (between 1 
    and nT inclusive).

    NOTE: Please use the previously implemented functions when applicable.
    Do not copy paste code from previous parts.

    Args:
        feature_matrix -  A numpy matrix describing the given data. Each row
            represents a single data point.
        labels - A numpy array where the kth element of the array is the
            correct classification of the kth row of the feature matrix.
        T - An integer indicating how many times the algorithm
            should iterate through the feature matrix.
        L - The lamba value being used to update the Pegasos
            algorithm parameters.

    Returns: A tuple where the first element is a numpy array with the value of
    the theta, the linear classification parameter, found after T
    iterations through the feature matrix and the second element is a real
    number with the value of the theta_0, the offset classification
    parameter, found after T iterations through the feature matrix.
    """
    # raise NotImplementedError
    
    current_theta, current_theta_0 = np.zeros(np.shape(feature_matrix)[1]), 0
    counter = 1
    for i in range(T):
        for j in range(len(feature_matrix)):
            k = random.randint(0,len(feature_matrix)-1)
            eta = 1/math.sqrt(counter)
            counter+= 1

           
            update = pegasos_single_step_update(feature_matrix[k],labels[k], L, eta, current_theta, current_theta_0)
            current_theta, current_theta_0 = update

    return (current_theta, current_theta_0)


### Part II

def classify(feature_matrix, theta, theta_0):
    """
    Section 2.8
    A classification function that uses theta and theta_0 to classify a set of
    data points.

    Args:
        feature_matrix - A numpy matrix describing the given data. Each row
            represents a single data point.
                theta - A numpy array describing the linear classifier.
        theta - A numpy array describing the linear classifier.
        theta_0 - A real valued number representing the offset parameter.

    Returns: A numpy array of 1s and -1s where the kth element of the array is the predicted
    classification of the kth row of the feature matrix using the given theta
    and theta_0.
    """
    label_array  = np.zeros(np.shape(feature_matrix)[0]) 
    for i in range(np.shape(feature_matrix)[0]):
        value = (np.dot(theta,feature_matrix[i]) + theta_0)
        if value > 0:
            label = 1
        else: 
            label = -1
        label_array[i] = label
    return label_array



        

def perceptron_accuracy(train_feature_matrix, val_feature_matrix, train_labels, val_labels, T):
    """
    Section 2.9
    Trains a linear classifier using the perceptron algorithm with a given T
    value. The classifier is trained on the train data. The classifier's
    accuracy on the train and validation data is then returned.

    Args:
        train_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        val_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        train_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the training
            feature matrix.
        val_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the validation
            feature matrix.
        T - The value of T to use for training with the perceptron algorithm.

    Returns: A tuple in which the first element is the (scalar) accuracy of the
    trained classifier on the training data and the second element is the accuracy
    of the trained classifier on the validation data.
    """
    # raise NotImplementedError
    perceptron_theta, perceptron_theta_0 = perceptron(train_feature_matrix, train_labels, T)
    classify_training_data = classify(train_feature_matrix,perceptron_theta, perceptron_theta_0)
    # print (type(train_feature_matrix), type(train_labels), "TYPES--------------")
    accuracy_training_data = accuracy(classify_training_data, train_labels)

    classify_validation_data = classify(val_feature_matrix, perceptron_theta, perceptron_theta_0)
    accuracy_validation_data = accuracy(classify_validation_data, val_labels)

    return (accuracy_training_data, accuracy_validation_data) 



    




def average_perceptron_accuracy(train_feature_matrix, val_feature_matrix, train_labels, val_labels, T):
    """
    Section 2.9
    Trains a linear classifier using the average perceptron algorithm with
    a given T value. The classifier is trained on the train data. The
    classifier's accuracy on the train and validation data is then returned.

    Args:
        train_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        val_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        train_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the training
            feature matrix.
        val_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the validation
            feature matrix.
        T - The value of T to use for training with the average perceptron
            algorithm.

    Returns: A tuple in which the first element is the (scalar) accuracy of the
    trained classifier on the training data and the second element is the accuracy
    of the trained classifier on the validation data.
    """
    # raise NotImplementedError
    perceptron_theta = average_perceptron(train_feature_matrix, train_labels, T)
    
    classify_training_data = classify(train_feature_matrix,perceptron_theta[0], perceptron_theta[1])
    classify_validation_data = classify(val_feature_matrix, perceptron_theta[0], perceptron_theta[1])
    
    accuracy_validation_data = accuracy(classify_validation_data, val_labels)
    accuracy_training_data = accuracy(classify_training_data, train_labels)

    return (accuracy_training_data, accuracy_validation_data) 

def pegasos_accuracy(train_feature_matrix, val_feature_matrix, train_labels, val_labels, T, L):
    """
    Section 2.9
    Trains a linear classifier using the pegasos algorithm
    with given T and L values. The classifier is trained on the train data.
    The classifier's accuracy on the train and validation data is then
    returned.

    Args:
        train_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        val_feature_matrix - A numpy matrix describing the training
            data. Each row represents a single data point.
        train_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the training
            feature matrix.
        val_labels - A numpy array where the kth element of the array
            is the correct classification of the kth row of the validation
            feature matrix.
        T - The value of T to use for training with the algorithm.
        L - The value of L to use for training with the Pegasos algorithm.

    Returns: A tuple in which the first element is the (scalar) accuracy of the
    trained classifier on the training data and the second element is the accuracy
    of the trained classifier on the validation data.
    """
    # raise NotImplementedError
    perceptron_theta = pegasos(train_feature_matrix, train_labels, T, L)
    classify_training_data = classify(train_feature_matrix,perceptron_theta[0], perceptron_theta[1])
    accuracy_training_data = accuracy(classify_training_data, train_labels)

    classify_validation_data = classify(val_feature_matrix, perceptron_theta[0], perceptron_theta[1])
    accuracy_validation_data = accuracy(classify_validation_data, val_labels)

    return (accuracy_training_data, accuracy_validation_data) 

def extract_words(input_string):
    """
    Helper function for bag_of_words()
    Inputs a text string
    Returns a list of lowercase words in the string.
    Punctuation and digits are separated out into their own words.
    """
    for c in punctuation + digits:
        input_string = input_string.replace(c, ' ' + c + ' ')

    return input_string.lower().split()

def bag_of_words(texts):
    """
    Inputs a list of string reviews
    Returns a dictionary of unique unigrams occurring over the input

    Feel free to change this code as guided by Section 3 (e.g. remove stopwords, add bigrams etc.)
    """
    f = open("stopwords.txt","r")
    stopwords = extract_words(f.read())

    dictionary = {} # maps word to unique index
    for text in texts:
        word_list = extract_words(text)
        for word in word_list:
            if word not in dictionary and word not in stopwords: 
                dictionary[word] = len(dictionary)
    
    # for text in texts:
    #     word_list = extract_words(text)
    #     for i in range(int(len(word_list)/)):
    #         i_bigram = word_list[i] + " " + word_list[i+1]
    #         if i_bigram not in dictionary:
    #             dictionary[i_bigram] = len(dictionary)


    return dictionary

# def remove_stop_words(dictionary):

#     """
#     remove stopwords from unigram dictionary
#     and return the modified dictionary
#     """
#     f = open("stopwords.txt", "r")

#     copy_dictionary = copy.deepcopy(dictionary)
#     stop_words = extract_words(f.read())
#     for word in dictionary:
#         if word in stop_words:
#             del copy_dictionary[word]    
#     return copy_dictionary
    

# print (remove_stop_words({}))



def extract_bow_feature_vectors(reviews, dictionary):
    """
    Inputs a list of string reviews
    Inputs the dictionary of words as given by bag_of_words
    Returns the bag-of-words feature matrix representation of the data.
    The returned matrix is of shape (n, m), where n is the number of reviews
    and m the total number of entries in the dictionary.
    """

    num_reviews = len(reviews)
    feature_matrix = np.zeros([num_reviews, len(dictionary)])

    for i, text in enumerate(reviews):  
        word_list = extract_words(text)
        for word in word_list:
            if word in dictionary:
                #modified to +=1 from =1 to include TF and weighing numbers + punctuation higher
                feature_matrix[i, dictionary[word]] +=1 
                if word in [",", ".", ] or word.isdigit():
                    feature_matrix[i, dictionary[word]] +=1

    return feature_matrix

def extract_additional_features(reviews):
    """x`
    Section 3.12
    Inputs a list of string reviews
    Returns a feature matrix of (n,m), where n is the number of reviews
    and m is the total number of additional features of your choice 

    YOU MAY CHANGE THE PARAMETERS
    """
    return np.ndarray((len(reviews), 0))

def extract_final_features(reviews, dictionary):
    """
    Section 3.12
    Constructs a final feature matrix using the improved bag-of-words and/or additional features
    """
    bow_feature_matrix = extract_bow_feature_vectors(reviews,dictionary)
    additional_feature_matrix = extract_additional_features(reviews)
    return np.hstack((bow_feature_matrix, additional_feature_matrix))

def accuracy(preds, targets):
    """
    Given length-N vectors containing predicted and target labels,
    returns the percentage and number of correct predictions.
    """
    # print (type(preds ==targets), "TYPE HERE---------------")
    # print (np.shape(preds), (len(targets), "SHAPES"))
    return (preds == targets).mean()

def normalize_vector(vector): 
    """
    Given a length N vector (a numpy ndarray), normalizes it and returns it with magnitude = 1
    """

    vector_magnitude = np.linalg.norm(vector)
    normalized_vector = vector/vector_magnitude
    return normalized_vector

