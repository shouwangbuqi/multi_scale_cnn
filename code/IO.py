import cPickle
import sys
import os
import pdb
import numpy
import theano
import theano.tensor as T

def unpickle(file):
    # Function to extract pickle files
    # extract pickle files
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

def load_cifar10(datapath, trainset_name, valset_name, mat2d_cols):
    """ Function used to load in cifar10 dataset. 
        datapath     : path to the dataset directory
        trainset_name: training set file names
        valset_name  : validation set file name
        mat2d_cols   : number of columns of the dataset
        returns the data and labels as numpy 2D arrays, for training and
            validation set.
        data_list_train, data_list_val  : 0 - 255
        label_list_train, label_list_val : 0 - 9, 10 classes
    """
    data_list_train = numpy.empty(shape=[0, mat2d_cols])
    label_list_train= numpy.empty(shape=[0,])

    for i in range(len(trainset_name)):
        temp_data = unpickle(datapath+trainset_name[i])
        temp_x    = temp_data['data']
        temp_y    = numpy.array(temp_data['labels'])                    
                                                                      
        data_list_train = numpy.append(data_list_train, temp_x, axis=0)
        label_list_train= numpy.append(label_list_train, temp_y, axis=0)

    temp_data = unpickle(datapath+valset_name)
    data_list_val = temp_data['data']
    label_list_val = numpy.array(temp_data['labels'])
    del temp_data

    return data_list_train, label_list_train, data_list_val, label_list_val

def share_data(data_x, data_y, borrow=True):
    # Function used to convert array and list into shared variables
    shared_x = theano.shared(numpy.asarray(data_x,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    shared_y = theano.shared(numpy.asarray(data_y,
                                           dtype=theano.config.floatX),
                             borrow=borrow)
    return shared_x, T.cast(shared_y, 'int32')
