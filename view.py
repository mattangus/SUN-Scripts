import cv2
import numpy as np
import argparse
import random
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", "-i", type=str, required=True)
    parser.add_argument("--num_classes", "-n", type=int, default=19)
    parser.add_argument("--ignore_label", "-l", nargs='+', type=int, default=[255])
    parser.add_argument("--out_dir", "-o", type=str, default="out")


    args = parser.parse_args()
    return args

def get_valid(annot, ignore_label):
    ne = [np.not_equal(annot, il) for il in ignore_label]
    validity_mask = ne.pop(0)
    for v in ne:
        validity_mask = np.logical_and(validity_mask, v)
    return validity_mask

def main():
    args = get_args()

    data = []
    with open(args.images, "r") as f:
        for line in f.readlines():
            data.append(line.strip().split(","))
    
    random.shuffle(data)

    num_classes = args.num_classes
    ignore_label = args.ignore_label
    out_dir = args.out_dir

    os.makedirs(out_dir, exist_ok=True)

    for img_pair in data:
        img = cv2.imread(img_pair[0])
        annot = cv2.imread(img_pair[1])

        print(img_pair[0] + ":", np.unique(annot))

        valid = get_valid(annot, ignore_label)
        #0 = ID, 1 = OOD
        ood_annot = np.logical_and(annot >= num_classes, valid).astype(np.uint8)
        ood_annot[np.logical_not(valid)] = 3

        disp = np.concatenate([img, (ood_annot*(255./3.)).astype(np.uint8)], 1)

        cv2.imshow("test", cv2.resize(disp, (1920, 1080)))
        resp = cv2.waitKey()
        if resp == 27:
            break
        if resp == ord("s"):
            cv2.imwrite(os.path.join(out_dir, os.path.basename(img_pair[1])), disp)
        


if __name__ == "__main__":
    main()