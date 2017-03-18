tfyarn
======

tfyarn simplifies the distributed TensorFlow programming model, for running
machine learning applications on Hadoop YARN clusters.

User Guide
----------

1. In your code: replace ``tf.train.ClusterSpec()`` with ``tfyarn.createClusterSpec()``
2. On your cluster: submit the application with `hops-tensorflow <https://github.com/tobiajo/hops/tree/develop/hops-tensorflow>`_

WORK IN PROGRESS
----------------

Not ready for usage, development is still in a very early stage.
