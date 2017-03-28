# MNIST

The orginal sources is:
- https://github.com/yahoo/TensorFlowOnSpark/blob/master/examples/mnist/tf/mnist_dist.py
- https://github.com/tensorflow/tensorflow/blob/master/tensorflow/tools/dist_test/python/mnist_replica.py

This is basicaly a clone of the TensorFlowOnSpark example.

## Try the example

1. To get the data set for this example, TFRecords or CSV, please follow [this guide](https://github.com/yahoo/TensorFlowOnSpark/wiki/GetStarted_YARN).
2. Clone and `mvn install`: https://github.com/tobiajo/hops-tensorflow/tree/develop
3. Locate _yarntf-submit_ in _hops-tensorflow/bin_.
3. Run distributed training:
```
yarntf-submit \
        --queue                         default \
        --workers                       3 \
        --pses                          1 \
        --memory                        1024 \
        --vcores                        1 \
        --main mnist.py \
        --args \
        --images mnist/tfr/train \
        --format tfr \
        --mode train \
        --model mnist_model
```
5. Run distributed inference:
```
yarntf-submit \
        --queue                         default \
        --workers                       3 \
        --pses                          1 \
        --memory                        1024 \
        --vcores                        1 \
        --main mnist.py \
        --args \
        --images mnist/tfr/test \
        --mode inference \
        --model mnist_model \
        --output mnist_predictions
```

Notes: the amount of memory is given in MB. For more arguments see `yarntf-submit --help`.
