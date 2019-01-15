# SUN-Scripts
Scripts for the SUN database: http://sun.cs.princeton.edu/ (Get the dataset [here](http://groups.csail.mit.edu/vision/SUN/releases/SUN2012.tar.gz))

## Files

**create_annot.py**

Used to create images from xml annotations, as well as a csv of the pairs generated.

**maps.py**

File containing the class mapping from SUN to Cityscapes

**view.py**

Using the genereated csv, view random pairs of generated images side by side.

## Usage

```
#download and extract dataset to <dataset_dir>
python3 create_annot.py -b <dataset_dir>
```

Based on the map images will be created in a new directory `<dataset_dir>/AnnotImg` with the same folder structure as the `<dataset_dir>/Images`.
