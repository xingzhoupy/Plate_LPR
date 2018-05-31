import os
import cv2
import numpy as np
import time
from hyperlpr_py3 import pipline as pp
from PIL import ImageFont,ImageDraw,Image

font = ImageFont.truetype(r'./Font/platech.ttf',80)

def SimpleRecognizePlateWithGui(image,filename):
    images = pp.detect.detectPlateRough(
        image, image.shape[0], top_bottom_padding_rate=0.1)

    res_set = []
    for j, plate in enumerate(images):
        plate, rect, origin_plate = plate
        plate = cv2.resize(plate, (136, 36 * 2))


        plate_color = "蓝"
        plate_type = pp.td.SimplePredict(plate)

        if (plate_type > 0) and (plate_type < 5):
            plate = cv2.bitwise_not(plate)
            plate_color = "黄"

        image_rgb = pp.fm.findContoursAndDrawBoundingBox(plate)

        image_rgb = pp.fv.finemappingVertical(image_rgb)
        pp.cache.verticalMappingToFolder(image_rgb)

        e2e_plate, e2e_confidence = pp.e2e.recognizeOne(image_rgb)
        #print("e2e:", e2e_plate, e2e_confidence)

        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        #print("校正", time.time() - t1, "s")

        t2 = time.time()
        # val = pp.segmentation.slidingWindowsEval(image_gray)
        # print val
        #print("分割和识别", time.time() - t2, "s")

        # if len(val) == 3:
        #     blocks, res, confidence = val
        #     if confidence / 7 > 0.7:
        #
        #         for i, block in enumerate(blocks):
        #
        #             block_ = cv2.resize(block, (24, 24))
        #             block_ = cv2.cvtColor(block_, cv2.COLOR_GRAY2BGR)
        #             image[j * 24:(j * 24) + 24, i * 24:(i * 24) + 24] = block_
        #             if image[j * 24:(j * 24) + 24,
        #                      i * 24:(i * 24) + 24].shape == block_.shape:
        #                 pass

        res_set.append([
                        rect,
                        plate_color,
                        e2e_plate,
                        e2e_confidence,
                        filename
                        ])

    return image, res_set

def recognize_and_show_one_image(path,flag):

    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    path = path.replace('\\','/')
    filename = path.rsplit('/',1)[-1]
    image,res_set = SimpleRecognizePlateWithGui(image,filename)
    image = draw_dialog(image,res_set,flag,path)
    return res_set

def draw_dialog(image,res_set,flag,path):
    # print(res_set)
    print(flag)
    if len(res_set) > 0:
        for res in res_set:
            curr_rect = res[0]
            y = int(curr_rect[1])
            x = int(curr_rect[0])
            h = int(curr_rect[1] + curr_rect[3])
            w = int(curr_rect[0] + curr_rect[2])
            image = cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 7)
            # cv2.imwrite(r'C:\Users\User\Desktop\ct_plate.jpg', image)
            img_PIL = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_PIL)
            draw.text((x,y-100),res[2], font=font, fill=(0,255,0))
            image = cv2.cvtColor(np.asarray(img_PIL),cv2.COLOR_RGB2BGR)
            path = path.replace('/', '\\')
            dir = path.rsplit('\\', 1)[0] + '\\temp'
            creat_dir(dir)
        cv2.imwrite(dir+'\\'+str(flag)+'.jpg',image)
        return image

def creat_dir(dir):
    # print(dir)
    if not os.path.exists(dir):
        os.mkdir(dir)

if __name__ == '__main__':
    recognize_and_show_one_image(r'C:\Users\User\Pictures\car\IMG_20180523_123619.jpg',0)