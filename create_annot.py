import cv2
import numpy as np
import libxml2 as xml
import glob
import argparse
import os
import sys
import matplotlib.pyplot as plt
import tqdm

import maps

parser = argparse.ArgumentParser()
parser.add_argument("--base_path", "-b", required=True)

args = parser.parse_args()

ANNOT_FILTER = os.path.join(args.base_path, "Annotations/**/*.xml")
OUT_FOLDER = os.path.join(args.base_path, "AnnotImg")

os.makedirs(OUT_FOLDER, exist_ok=True)

dbg = True

def break_assert(cond, statement):
    if not cond:
        print(statement)
        if dbg:
            import pdb; pdb.set_trace()
        else:
            sys.exit()

def extract_meta(xml_node):
    #get filename
    filenames = xml_node.xpathEval("//filename")
    break_assert(len(filenames) == 1, "found more than one filename")
    filename = filenames[0].content.strip()

    #get folder path
    folders = xml_node.xpathEval("//folder")
    break_assert(len(folders) == 1, "found more than one folder")
    folder = folders[0].content.strip()
    #get image size
    imagesizes = xml_node.xpathEval("//imagesize")
    if len(imagesizes) == 0:
        #print("malformed document", xml_node)
        return None, folder, filename
    break_assert(len(imagesizes) == 1, "found more than one image size")
    imagesize = imagesizes[0]
    all_rows = imagesize.xpathEval("nrows")
    all_cols = imagesize.xpathEval("ncols")
    break_assert(len(all_rows) == 1, "found more than one nrows")
    break_assert(len(all_cols) == 1, "found more than one ncols")
    rows = int(all_rows[0].content.strip())
    cols = int(all_cols[0].content.strip())

    return (rows, cols), folder, filename

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

    return name.lower(), np.array(pts), username.lower()

def main():
    xml_files = glob.glob(ANNOT_FILTER, recursive=True)

    not_found = set()

    all_out_files = []

    for xml_path in tqdm.tqdm(xml_files):
        with open(xml_path, "r") as f:
            # remove invalid char in name
            content = f.read().replace("\x1a", "")

        doc = xml.parseDoc(content)
        #doc = xml.parseFile(xml_path)
        ctxt = doc.xpathNewContext()

        size, folder, filename = extract_meta(ctxt)
        folder = os.path.join(OUT_FOLDER, folder)
        out_file = os.path.join(folder, filename.replace("jpg", "png"))
        if size is None:
            continue
        
        img_file = os.path.join(folder.replace("AnnotImg", "Images"), filename)
        if not os.path.exists(img_file):
            continue

        if np.prod(size) < 640*640:
            continue

        objects = ctxt.xpathEval("//object")

        annot_img = np.ones(size)*255

        types = set()

        has_values = False

        for obj in objects:
            name, pts, username = extract_object(obj)
            types.add(name)
            if username == "anonymous":
                continue
            name = name.replace("crop", "").replace("occluded", "").strip()
            if name not in maps.sun_to_id:
                if name not in not_found:
                    print("could not find", name)
                    not_found.add(name)
                continue

            has_values = True

            colour = maps.sun_to_id[name]
            annot_img = cv2.fillPoly(annot_img, pts =[pts], color=colour)

        # print(types, "\n")
        # cv2.imshow("test", (255*annot_img/np.max(annot_img)).astype(np.uint8))
        # cv2.waitKey()
        if has_values:
            os.makedirs(folder, exist_ok=True)
            cv2.imwrite(out_file, annot_img.astype(np.uint8))
            all_out_files.append(img_file + "," + out_file)

        # print("done")
        # i+=1
        # print(i, end="\r")

    print(len(all_out_files))
    with open('all_sun_annot.txt', 'w') as f:
        f.write('\n'.join(all_out_files))

if __name__ == "__main__":
    main()