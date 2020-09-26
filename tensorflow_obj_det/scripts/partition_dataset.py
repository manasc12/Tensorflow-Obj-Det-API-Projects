""" usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-x]

Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -x XML_DIR, --xml_dir XML_DIR
                        Path to the folder where the input .xml files are stored.
  -t TXT_DIR, --txt_dir TXT_DIR
                        Path to the folder where the input .txt files are stored.
  -i IMAGEDIR, --image_dir IMAGEDIR
                        Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
  -r TEST_SIZE_RATIO, --ratio TEST_SIZE_RATIO
                        The ratio of the number of test images over the total number of images. The default is 0.1.
"""
import os
import re
from shutil import copyfile,move
import argparse
import math
import random

def sanity_check(dir):
    for file in os.listdir(dir):
        if (len(str.split(file, ".")) > 2):
            raise Exception(
                "{1}/{0} --- The file name has 2 dots. \n Please make sure there should only be one dot in the file name.".format(
                    file, dir))

def iterate_dir(source, dest, ratio,txt_or_xml_dir,txt_or_xml):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    images = [f for f in os.listdir(source)
              if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png|.webp)$', f)]

    num_images = len(images)
    num_test_images = math.ceil(ratio*num_images)

    for i in range(num_test_images):
        idx = random.randint(0, len(images)-1)
        filename = images[idx]
        move(os.path.join(source, filename),os.path.join(test_dir, filename))
        tx_filename = os.path.splitext(filename)[0]+txt_or_xml
        move(os.path.join(txt_or_xml_dir, tx_filename),os.path.join(test_dir,tx_filename))
        images.remove(images[idx])

    for filename in images:
        move(os.path.join(source, filename),os.path.join(train_dir, filename))
        tx_filename = os.path.splitext(filename)[0]+txt_or_xml
        move(os.path.join(txt_or_xml_dir, tx_filename),os.path.join(train_dir, tx_filename))


def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "-x",
        "--xml_dir",
        help="Path to the folder where the input .xml files are stored.",
        type=str
    )
    parser.add_argument(
        "-t",
        "--txt_dir",
        help="Path to the folder where the input .txt files are stored.",
        type=str
    )
    parser.add_argument(
        '-i', '--image_dir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the train and test dirs should be created. '
             'Defaults to the same directory as IMAGEDIR.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-r', '--ratio',
        help='The ratio of the number of test images over the total number of images. The default is 0.1.',
        default=0.1,
        type=float)

    args = parser.parse_args()

    if (args.xml_dir is None and args.txt_dir is None):
        raise Exception("Both of xml_dir and txt_dir cant be None. At least provide one of them.")
    elif (args.xml_dir is not None and args.txt_dir is not None):
        raise Exception("Provide only one path. We cannot process both the folders")

    if args.image_dir is None and args.xml_dir is not None:
        args.image_dir = args.xml_dir
    elif args.image_dir is None:
        args.image_dir = args.txt_dir

    txt_or_xml_dir=''
    txt_or_xml=''
    if args.xml_dir is not None:
        sanity_check(args.xml_dir)
        txt_or_xml_dir=args.xml_dir
        txt_or_xml='.xml'
    else:
        sanity_check(args.txt_dir)
        txt_or_xml_dir = args.txt_dir
        txt_or_xml = '.txt'

    if args.outputDir is None:
        args.outputDir = args.imageDir



    # Now we are ready to start the iteration
    iterate_dir(args.image_dir, args.outputDir, args.ratio,txt_or_xml_dir,txt_or_xml)


if __name__ == '__main__':
    main()