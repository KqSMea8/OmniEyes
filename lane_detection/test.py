#!/usr/bin/env python3
import os
import argparse
import math
import tensorflow as tf
import numpy as np

import cv2
try:
    from cv2 import cv2
except ImportError:
    pass

import global_config
from data_processor import TestingDataset
from model import lanenet_merge_model

CFG = global_config.cfg

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, help='The path of the folder that contains all of the testing images')
parser.add_argument('--model_weight_path', type=str, help='The model weights path')
parser.add_argument('--batch_size', type=int, help='The batch size of testing images', default=1)
parser.add_argument('--save_dir', type=str, help='The path to save results', default=None)
args = parser.parse_args()

def main():

    test_dataset = TestingDataset(data_dir=args.data_dir, batch_size=args.batch_size)
    input_tensor = tf.placeholder(dtype=tf.string, shape=[None], name='input_tensor')
    imgs = tf.map_fn(test_dataset.process_img, input_tensor, dtype=tf.float32)
    phase_tensor = tf.constant('test', tf.string)

    net = lanenet_merge_model.LaneNet()
    binary_seg_ret, instance_seg_ret = net.test_inference(imgs, phase_tensor, 'lanenet_loss')
    initial_var = tf.global_variables()
    final_var = initial_var[:-1]
    saver = tf.train.Saver(final_var)

    # Set sess configuration
    sess_config = tf.ConfigProto(device_count={'GPU': 1})
    sess_config.gpu_options.per_process_gpu_memory_fraction = CFG.TEST.GPU_MEMORY_FRACTION
    sess_config.gpu_options.allow_growth = CFG.TRAIN.TF_ALLOW_GROWTH
    sess_config.gpu_options.allocator_type = 'BFC'
    sess = tf.Session(config=sess_config)
    with sess.as_default():
        sess.run(tf.global_variables_initializer())
        saver.restore(sess=sess, save_path=args.model_weight_path)

        file_list = os.listdir(args.data_dir)
        file_list = [ f for f in file_list if '.jpg' in f ]
        num_images = len(file_list)


        for i in range(math.ceil(num_images / args.batch_size)):
            print('Processing batch {}'.format(i))
            paths = test_dataset.next_batch()
            instance_seg_image, existence_output = sess.run([binary_seg_ret, instance_seg_ret],
                                                            feed_dict={input_tensor: paths})
            for count, image_name in enumerate(paths):            
                #txt_file = open(os.path.join(args.save_dir, os.path.basename(image_name).split('.')[0] + '.txt'), 'w')
                for lane_count in range(CFG.NUM_CLASSES):
                    #cv2.imwrite(os.path.join(args.save_dir, os.path.basename(image_name).split('.')[0] + '_' + str(lane_count + 1) + '.png'),
                    #        (instance_seg_image[count, :, :, lane_count + 1] * 255).astype(int))
                    
                    #txt_file.write(str(existence_output[count, lane_count])+' ')

                    img = cv2.resize((instance_seg_image[count, :, :, lane_count + 1] * 255).astype('float32'), (1640, 590), interpolation=cv2.INTER_CUBIC)

                    if lane_count == 0:
                        total_seg_image = img
                    else:
                        total_seg_image += img

                #txt_file.close()

                raw_image = cv2.imread(image_name)
                total_seg_image = cv2.cvtColor(total_seg_image, cv2.COLOR_GRAY2RGB)
                concat_image = np.concatenate((total_seg_image, raw_image), axis=0)

                cv2.imwrite(os.path.join(args.save_dir, os.path.basename(image_name).split('.')[0] + '_concat.png'), concat_image)
                #cv2.imwrite(os.path.join(args.save_dir, os.path.basename(image_name).split('.')[0] + '_total.png'), total_seg_image)
    sess.close()
    return

if __name__ == '__main__':

    if args.save_dir is not None and not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    main()