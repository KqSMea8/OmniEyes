import os 
import tensorflow as tf
import global_config

CFG = global_config.cfg

class TestingDataset(object):

    def __init__(self, data_dir, batch_size):

        self.img_list = os.listdir(data_dir)
        self.img_list = [ f for f in self.img_list if '.jpg' in f ]
        self.img_list = [ os.path.join(data_dir, img) for img in self.img_list ]
        self.batch_size = batch_size
        self.next_batch_loop_count = 0

    @staticmethod
    def process_img(img_path):
        img_raw = tf.read_file(img_path)
        img_decoded = tf.image.decode_jpeg(img_raw, channels=3)
        img_resized = tf.image.resize_images(img_decoded, [CFG.TRAIN.IMG_HEIGHT, CFG.TRAIN.IMG_WIDTH],
                                             method=tf.image.ResizeMethod.BICUBIC)
        img_casted = tf.cast(img_resized, tf.float32)

        # Convert RGB to BGR
        img_casted = img_casted[..., ::-1]

        return tf.subtract(img_casted, CFG.VGG_MEAN)

    def next_batch(self):
        idx_start = self.batch_size * self.next_batch_loop_count
        idx_end = self.batch_size * (self.next_batch_loop_count + 1)
        if idx_end > len(self.img_list):
            idx_end = len(self.img_list)
        self.next_batch_loop_count += 1
        return self.img_list[idx_start:idx_end]
