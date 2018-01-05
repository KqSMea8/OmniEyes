from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import glob
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import tensorflow as tf
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

np.random.seed(1)

# SETTINGS
label_csv_file = 'all_labels.csv' # output .csv file name, default path is under data folder
train_ratio = 0.8 # ratio of training data
output_path_train = 'data/train.record'
output_path_test = 'data/test.record'

def xml_to_csv(path):
    xml_list = []
    image_count = 0
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
        image_count += 1
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df, image_count

def ProcessXml(label_csv_file):
    image_path = os.path.join(os.getcwd(), 'annotations')
    csv_path = os.path.join(os.getcwd(), 'data/' + label_csv_file)
    xml_df, image_count = xml_to_csv(image_path)
    xml_df.to_csv(csv_path, index=None)
    print('[INFO] Successfully converted xml to csv, total {} images.',image_count)
    return image_count

def SplitData(image_count, train_ratio):
    full_labels = pd.read_csv('data/' + label_csv_file)
    train_size = int(image_count*train_ratio)

    grouped = full_labels.groupby('filename')
    grouped.apply(lambda x: len(x)).value_counts()
    gb = full_labels.groupby('filename')
    grouped_list = [gb.get_group(x) for x in gb.groups]

    train_index = np.random.choice(len(grouped_list), size=train_size, replace=False)
    test_index = np.setdiff1d(list(range(image_count)), train_index)

    train = pd.concat([grouped_list[i] for i in train_index])
    test = pd.concat([grouped_list[i] for i in test_index])

    train.to_csv('data/train_labels.csv', index=None)
    test.to_csv('data/test_labels.csv', index=None)
    print('[INFO] Successfully seperate train and validation data.')

def ReadLabelClass():
    with open('data/label_class.pbtxt','r') as f:
        data = f.read().split('\n')
        label_dict = {}
        for i,v in enumerate(data):
            if 'name' in v:
                name = v.split('name:')[1].strip(' ').strip('\'')
                ID = data[i-1].split('id:')[1].strip(' ')
                label_dict[name] = int(ID)
    return label_dict

def class_text_to_int(row_label, label_dict):
    return label_dict[row_label] if row_label in label_dict else 0

# transform to tf record format

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

def create_tf_example(group, path, label_dict):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class'],label_dict))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def main(output_path_train, output_path_test):
    image_count = ProcessXml(label_csv_file)
    SplitData(image_count, train_ratio)
    label_dict = ReadLabelClass()

    writer = tf.python_io.TFRecordWriter(output_path_train)
    path = os.path.join(os.getcwd(), 'images')
    examples = pd.read_csv('data/train_labels.csv')
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path, label_dict)
        writer.write(tf_example.SerializeToString())
    writer.close()
    output_path = os.path.join(os.getcwd(), output_path_train)
    print('[INFO] Successfully created the TFRecords: {}'.format(output_path))

    writer = tf.python_io.TFRecordWriter(output_path_test)
    path = os.path.join(os.getcwd(), 'images')
    examples = pd.read_csv('data/test_labels.csv')
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path, label_dict)
        writer.write(tf_example.SerializeToString())
    writer.close()
    output_path = os.path.join(os.getcwd(), output_path_test)
    print('[INFO] Successfully created the TFRecords: {}'.format(output_path))

if __name__ == '__main__':
    main(output_path_train, output_path_test)
