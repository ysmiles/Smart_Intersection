# Image recognition from Google Inception

Part of this introduction is from original [Tensorflow GitHub repository](
https://github.com/tensorflow/models/tree/master/research/inception).
It is licensed under [Apache license 2.0](https://github.com/tensorflow/tensorflow/blob/master/LICENSE).

The car brand data is copyrighted. They are at the training machine and no link is put here.

## Installation of Tensorflow

Install Tensorflow at a linux server or desktop is not that hard. Here is a summary of installation bach commands from official guide.

```bash
# for ubuntu
sudo apt-get install python3-pip python3-dev python-virtualenv # for Python 3.n
virtualenv --system-site-packages -p python3 ~/tensorflow # for Python 3.n
source ~/tensorflow/bin/activate # bash, sh, ksh, or zsh
# Assume at least have python 3.5
# For GPU usage, use tensorflow-gpu
(tensorflow)$ pip3 install --upgrade tensorflow     # for Python 3.n
```

One note here is to use `virtualenv`, which provide a separated python environment to tensorflow.
The goodness of this is that inside this environment, we do not need to care python or python3, pip or pip3, etc.
In my case, it only has python 3 inside.
Because linux servers always have some python 2 version(s), which is quite annoying for stricting version every time. 
So this `virtualenv` does help.
Just remember to `activate` it as showed above.

## Docker usage at remote server

The main training work is performed at a server in docker container.

For basic docker usage, please refer my blog [article 1](http://ysmiles.com/2017/10/05/Run-a-basic-gRPC-example-with-Docker/) and [article 2](http://ysmiles.com/2017/12/06/HTTP-server-inside-a-docker-container/).

For TensorFlow usage, it is just similar as this command:

```bash
nvidia-docker run -it gcr.io/tensorflow/tensorflow:latest-gpu bash
```

## Architecture

Code in this directory
demonstrates how to use TensorFlow to train and evaluate a type of convolutional
neural network (CNN) on this academic data set. In particular, we demonstrate
how to train the Inception v3 architecture as specified in:

_Rethinking the Inception Architecture for Computer Vision_

Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, Zbigniew
Wojna

http://arxiv.org/abs/1512.00567

This network achieves 21.2% top-1 and 5.6% top-5 error for single frame
evaluation with a computational cost of 5 billion multiply-adds per inference
and with using less than 25 million parameters. Below is a visualization of the
model architecture.
`
![Inception-v3 Architecture](inception_v3_architecture.png)

## Description of codes

The code provides three core binaries for:

*   Training an Inception v3 network from scratch across multiple GPUs and/or
    multiple machines using the car brand training data set.
*   Evaluating an Inception v3 network using the car brand Challenge
    validation data set.
*   Retraining an Inception v3 network on a novel task and back-propagating the
    errors to fine tune the network weights.

The training procedure employs synchronous stochastic gradient descent across multiple GPUs. The user may specify the number of GPUs they wish to harness. The synchronous training performs batch-splitting by dividing a given batch across multiple GPUs.

## Training

The training procedure is encapsulated by this diagram of how operations and
variables are placed on CPU and GPUs respectively.

<div style="width:40%; margin:auto; margin-bottom:10px; margin-top:20px;">
  <img style="width:100%" src="https://www.tensorflow.org/images/Parallelism.png">
</div>

Each tower computes the gradients for a portion of the batch and the gradients
are combined and averaged across the multiple towers in order to provide a
single update of the Variables stored on the CPU.

We chose a fine-tuned model, i.e. the flower_train, as our model to develop further.
The usage is as follow, for easy use, we did not change the binary name, but modified the data set name and folder name.

```bash
# Build the model. Note that we need to make sure the TensorFlow is ready to
# use before this as this command will not build TensorFlow.
cd tensorflow-models/inception
bazel build //inception:flowers_train

# Run the fine-tuning on the flowers data set starting from the pre-trained
# Imagenet-v3 model.
bazel-bin/inception/flowers_train \
    --train_dir=/share_folder/220Proj/car_brand_identify/car_train \
    --data_dir=/share_folder/220Proj/car_brand_identify/TFRecords-data \
    --pretrained_model_checkpoint_path=/usr/local/lib/python3.5/dist-packages/inception-v3/model.ckpt-157585 \
    --fine_tune=True \  
    --initial_learning=0.001 \
    --input_queue_memory_factor=1 \
    --max_steps=10000
```

For preparing data, run `build_image_data` by running the following command line:

```bash
# location to where to save the TFRecord data.
OUTPUT_DIRECTORY=$HOME/my-custom-data/

# build the preprocessing script.
cd tensorflow-models/inception
bazel build //inception:build_image_data

# convert the data.
bazel-bin/inception/build_image_data \
  --train_directory="${TRAIN_DIR}" \
  --validation_directory="${VALIDATION_DIR}" \
  --output_directory="${OUTPUT_DIRECTORY}" \
  --labels_file="${LABELS_FILE}" \
  --train_shards=128 \
  --validation_shards=24 \
  --num_threads=8
```

where the `$OUTPUT_DIRECTORY` is the location of the sharded `TFRecords`. The
`$LABELS_FILE` will be a text file that is read by the script that provides
a list of all of the labels.


## Evaluation

The training script will only reports the loss. To evaluate the quality of the
fine-tuned model, we can run `flowers_eval`:

```bash
# Build the model. Note that we need to make sure the TensorFlow is ready to
# use before this as this command will not build TensorFlow.
cd tensorflow-models/inception
bazel build //inception:flowers_eval

# Evaluate the fine-tuned model on a hold-out of the flower data set.
bazel-bin/inception/flowers_eval \
    --eval_dir=/share_folder/220Proj/car_brand_identify/car_eval \
    --data_dir=/share_folder/220Proj/car_brand_identify/test_data \
    --subset=validation \
    --num_examples=1 \
    --checkpoint_dir=/share_folder/220Proj_bak/car_brand_identify/car_train \
    --input_queue_memory_factor=1 \
    --run_once \
    --batch_size=1
```

