import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.misc
import tensorflow as tf
from PIL import Image
from scipy.stats import multivariate_normal
import cv2

n_classes = 20
# colour map
label_colours = [(0, 0, 0)
    , (128, 0, 0), (255, 0, 0), (0, 85, 0), (170, 0, 51), (255, 85, 0), (0, 0, 85), (0, 119, 221), (85, 85, 0),
                 (0, 85, 85), (85, 51, 0), (52, 86, 128), (0, 128, 0)
    , (0, 0, 255), (51, 170, 221), (0, 255, 255), (85, 255, 170), (170, 255, 85), (255, 255, 0), (255, 170, 0)]

# label_colours = [(0,0,0)
#                 # 0=background
#                 ,(128,0,0), (0,128,0), (128,128,0), (0,0,128), (128,0,128), (0,128,128)]
#                 # 1=head, 2=torso, 3=upper arm, 4=lower arm, 5=upper leg, # 6=lower leg
# image mean
IMG_MEAN = np.array((104.00698793, 116.66876762, 122.67891434), dtype=np.float32)


def decode_labels(mask, num_images=1, num_classes=21):
    """Decode batch of segmentation masks.
    
    Args:
      mask: result of inference after taking argmax.
      num_images: number of images to decode from the batch.
      num_classes: number of classes to predict (including background).
    
    Returns:
      A batch with num_images RGB images of the same size as the input. 
    """
    n, h, w, c = mask.shape
    assert (n >= num_images), 'Batch size %d should be greater or equal than number of images to save %d.' % (
    n, num_images)
    outputs = np.zeros((num_images, h, w, 3), dtype=np.uint8)
    for i in range(num_images):
        img = Image.new('RGB', (len(mask[i, 0]), len(mask[i])))
        pixels = img.load()
        for j_, j in enumerate(mask[i, :, :, 0]):
            for k_, k in enumerate(j):
                if k < num_classes:
                    pixels[k_, j_] = label_colours[k]
        outputs[i] = np.array(img)
    return outputs


def prepare_label(input_batch, new_size, one_hot=True):
    """Resize masks and perform one-hot encoding.

    Args:
      input_batch: input tensor of shape [batch_size H W 1].
      new_size: a tensor with new height and width.

    Returns:
      Outputs a tensor of shape [batch_size h w 21]
      with last dimension comprised of 0's and 1's only.
    """
    with tf.name_scope('label_encode'):
        input_batch = tf.image.resize_nearest_neighbor(input_batch,
                                                       new_size)  # as labels are integer numbers, need to use NN interp.
        input_batch = tf.squeeze(input_batch, squeeze_dims=[3])  # reducing the channel dimension.
        if one_hot:
            input_batch = tf.one_hot(input_batch, depth=n_classes)
    return input_batch


def inv_preprocess(imgs, num_images):
    """Inverse preprocessing of the batch of images.
       Add the mean vector and convert from BGR to RGB.

    Args:
      imgs: batch of input images.
      num_images: number of images to apply the inverse transformations on.

    Returns:
      The batch of the size num_images with the same spatial dimensions as the input.
    """
    n, h, w, c = imgs.shape
    assert (n >= num_images), 'Batch size %d should be greater or equal than number of images to save %d.' % (
    n, num_images)
    outputs = np.zeros((num_images, h, w, c), dtype=np.uint8)
    for i in range(num_images):
        outputs[i] = (imgs[i] + IMG_MEAN)[:, :, ::-1].astype(np.uint8)
    return outputs


def save(saver, sess, logdir, step):
    '''Save weights.   
    Args:
     saver: TensorFlow Saver object.
     sess: TensorFlow session.
     logdir: path to the snapshots directory.
     step: current training step.
    '''
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    model_name = 'model.ckpt'
    checkpoint_path = os.path.join(logdir, model_name)

    if not os.path.exists(logdir):
        os.makedirs(logdir)
    saver.save(sess, checkpoint_path, global_step=step)
    print('The checkpoint has been created.')


def load(saver, sess, ckpt_path):
    '''Load trained weights.
    
    Args:
      saver: TensorFlow saver object.
      sess: TensorFlow session.
      ckpt_path: path to checkpoint file with parameters.
    '''
    ckpt = tf.train.get_checkpoint_state(ckpt_path)
    if ckpt and ckpt.model_checkpoint_path:
        ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
        saver.restore(sess, os.path.join(ckpt_path, ckpt_name))
        print("Restored model parameters from {}".format(ckpt_name))
        return True
    else:
        return False


def resize_image(image, expected_size, pad_value, ret_params=False, mode=cv2.INTER_LINEAR):
    """
    image (ndarray) with either shape of [H,W,3] for RGB or [H,W] for grayscale.
    Padding is added so that the content of image is in the center.
    """
    h, w = image.shape[:2]
    if w > h:
        w_new = int(expected_size)
        h_new = int(h * w_new / w)
        image = cv2.resize(image, (w_new, h_new), interpolation=mode)

        pad_up = (w_new - h_new) // 2
        pad_down = w_new - h_new - pad_up
        if len(image.shape) == 3:
            pad_width = ((pad_up, pad_down), (0, 0), (0, 0))
            constant_values = ((pad_value, pad_value), (0, 0), (0, 0))
        elif len(image.shape) == 2:
            pad_width = ((pad_up, pad_down), (0, 0))
            constant_values = ((pad_value, pad_value), (0, 0))

        image = np.pad(
            image,
            pad_width=pad_width,
            mode="constant",
            constant_values=constant_values,
        )
        if ret_params:
            return image, pad_up, 0, h_new, w_new
        else:
            return image

    elif w < h:
        h_new = int(expected_size)
        w_new = int(w * h_new / h)
        image = cv2.resize(image, (w_new, h_new), interpolation=mode)

        pad_left = (h_new - w_new) // 2
        pad_right = h_new - w_new - pad_left
        if len(image.shape) == 3:
            pad_width = ((0, 0), (pad_left, pad_right), (0, 0))
            constant_values = ((0, 0), (pad_value, pad_value), (0, 0))
        elif len(image.shape) == 2:
            pad_width = ((0, 0), (pad_left, pad_right))
            constant_values = ((0, 0), (pad_value, pad_value))

        image = np.pad(
            image,
            pad_width=pad_width,
            mode="constant",
            constant_values=constant_values,
        )
        if ret_params:
            return image, 0, pad_left, h_new, w_new
        else:
            return image

    else:
        image = cv2.resize(image, (expected_size, expected_size), interpolation=mode)
        if ret_params:
            return image, 0, 0, expected_size, expected_size
        else:
            return image
