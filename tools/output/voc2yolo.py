import xml.etree.ElementTree as ET
import os
import shutil


# The script is based on https://github.com/AlexeyAB/darknet/blob/master/scripts/voc_label.py

sets = ['train', 'val', 'test']

classes = ["Car", "OtherVehicle"]


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id, set):
    in_file = open('Annotations/%s.xml' % image_id)
    out_file = open('labels/%s/%s.txt' % (set, image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = 0
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


wd = '.'

for image_set in sets:
    if not os.path.exists('images/%s' % (image_set)):
        os.makedirs('images/%s' % (image_set))
    if not os.path.exists('labels/%s' % (image_set)):
        os.makedirs('labels/%s' % (image_set))
    image_ids = open('ImageSets/Main/%s.txt' % image_set).read().strip().split()
    # list_file = open('%s.txt' % image_set, 'w')
    for image_id in image_ids:
        # list_file.write('%s/JPEGImages/%s.jpg\n' % (wd, image_id))
        convert_annotation(image_id, image_set)
        shutil.copy2("JPEGImages/%s.jpg" % image_id, "images/%s/%s.jpg"%(image_set, image_id))
    # list_file.close()

