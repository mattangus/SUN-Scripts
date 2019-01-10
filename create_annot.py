import cv2
import numpy as np
import libxml2 as xml
import glob
import argparse
import os
import sys
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--base_path", "-b", required=True)

args = parser.parse_args()

ANNOT_FILTER = os.path.join(args.base_path, "Annotations/**/*.xml")

dbg = True

def break_assert(cond, statement):
    if not cond:
        print(statement)
        if dbg:
            import pdb; pdb.set_trace()
        else:
            sys.exit()

def extract_imagesize(xml_node):
    #get image size
    imagesizes = xml_node.xpathEval("//imagesize")
    if len(imagesizes) == 0:
        #print("malformed document", xml_node)
        return None
    break_assert(len(imagesizes) == 1, "found more than one image size")
    imagesize = imagesizes[0]
    all_rows = imagesize.xpathEval("nrows")
    all_cols = imagesize.xpathEval("ncols")
    break_assert(len(all_rows) == 1, "found more than one nrows")
    break_assert(len(all_cols) == 1, "found more than one ncols")
    rows = int(all_rows[0].content.strip())
    cols = int(all_cols[0].content.strip())

    return (rows, cols)

def extract_object(xml_node):
    #get name
    names = xml_node.xpathEval("name")

    break_assert(len(names) == 1, "found more than one name")
    name = names[0].content.strip()

    #get the polygon
    polygons = xml_node.xpathEval("polygon")
    break_assert(len(polygons) == 1, "found more than one polygon")
    polygon = polygons[0]
    xs = polygon.xpathEval("pt/x")
    ys = polygon.xpathEval("pt/y")
    pts = [(int(x.content.strip()), int(y.content.strip())) for x,y in zip(xs,ys)]

    #get the username
    usernames = polygon.xpathEval("username")
    break_assert(len(usernames) == 1, "found more than one username")
    username = usernames[0].content.strip()

    return name, pts, username

xml_files = glob.iglob(ANNOT_FILTER, recursive=True)

all_sizes = []
i = 0

for xml_path in xml_files:
    with open(xml_path, "r") as f:
        # remove invalid char in name
        content = f.read().replace("\x1a", "")
    
    doc = xml.parseDoc(content)
    #doc = xml.parseFile(xml_path)
    ctxt = doc.xpathNewContext()

    size = extract_imagesize(ctxt)
    if size is None:
        continue


    if np.prod(size) > 640*640:
        all_sizes.append(np.prod(size))
        # import pdb; pdb.set_trace()
        i+=1
        print(i, end="\r")
        continue
    else:
        continue

    objects = ctxt.xpathEval("//object")
    for obj in objects:
        name, pts, username = extract_object(obj)

        if username == "anonomys":
            continue

    import pdb; pdb.set_trace()
    print("done")

plt.hist(all_sizes, 1000)
plt.show()