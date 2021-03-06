"""A very simple UCI classifier.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

""" Reference: Tensorflow documentation/tutorial https://www.tensorflow.org/versions/r0.11/tutorials/mnist/beginners/index.html"""

import argparse

# Import data
import input_data

import tensorflow as tf

FLAGS = None

uci = input_data.read_data_sets("/tmp/", one_hot=True)

size = 64

# Create the model
x = tf.placeholder(tf.float32, [None, input_data.size])
W = tf.Variable(tf.zeros([input_data.size, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.matmul(x, W) + b

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

sess = tf.InteractiveSession()
# Train
tf.initialize_all_variables().run()
for _ in range(1000):
  batch_xs, batch_ys = uci.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: uci.test.images,
                                    y_: uci.test.labels}))
