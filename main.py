import os
import json
import cv2
from PIL import Image

"""
1. BIC 또는 TYPESIZE 
바운딩 크기만큼 이미지 크롭해 저장해야함

2. 해당 이미지명 \t 실제 텍스트값  저장해야함

굳굳

"""

images_path = "D:/hackathon/hackathon/"

def find_first_point(points) :
    y_min = 99999999
    ymin_index = -1
    i = 0

    first_index = -1
    for point in points :
        if point[1] < y_min :
            y_min = point[1]
            ymin_index = i
        i += 1

    if ymin_index < 2 :
        if points[ymin_index][0] < points[1 - ymin_index][0] :
            first_index = ymin_index
        else :
            first_index = 1 - ymin_index
    else :
        if ymin_index == 2 :
            if points[ymin_index][0] < points[3][0] :
                first_index = ymin_index
            else :
                first_index = 3
        elif ymin_index == 3 :
            if points[ymin_index][0] < points[2][0] :
                first_index = ymin_index
            else :
                first_index = 2

    if first_index != -1 :
        return first_index

def find_last_point(points) :
    y_max = 0
    ymax_index = -1
    i = 0

    last_index = -1
    for point in points :
        if point[1] > y_max :
            y_max = point[1]
            ymax_index = i
        i += 1

    if ymax_index < 2 :
        if points[ymax_index][0] > points[1 - ymax_index][0] :
            last_index = ymax_index
        else :
            last_index = 1 - ymax_index
    else :
        if ymax_index == 2 :
            if points[ymax_index][0] > points[3][0] :
                last_index = ymax_index
            else :
                last_index = 3
        elif ymax_index == 3 :
            if points[ymax_index][0] > points[2][0] :
                last_index = ymax_index
            else :
                last_index = 2

    if last_index != -1 :
        return last_index

def change_points(x1, y1, x2, y2) :
    temp_x = x2
    temp_y = y2
    x2 = x1
    y2 = y1
    x1 = temp_x
    y1 = temp_y

    return x1, y1, x2, y2

def mouse_callback(event, x, y, flags, param): 
    print("마우스 이벤트 발생, x:", x ," y:", y) # 이벤트 발생한 마우스 위치 출력

def crop_image_horizontal(points, image_name,bbox_id ,i) :
    # image = cv2.imread(images_path + image_name + ".jpg")
    image = Image.open(images_path + image_name + ".jpg")

    first_index = find_first_point(points)
    last_index = find_last_point(points)

    start_x = points[first_index][0]
    start_y = points[first_index][1]

    last_x = points[last_index][0]
    last_y = points[last_index][1]

    print(f"s_x : {start_x}, s_y {start_y}, l_x : {last_x}, l_y : {last_y}")
    
    if bbox_id == "BIC" :
        if start_x > last_x : 
            start_x, start_y, last_x, last_y = change_points(start_x, start_y, last_x, last_y)

        if last_y < start_y :
            distance = (start_y - last_y) * 1.2
            start_y -= distance
            last_y += distance
        
        if last_y - start_y < 30 :
            start_y -= 30
            last_y += 30
        
        if last_x - start_x < 20 :
            start_x -= 10
            last_x += 10
    else :
        if start_x > last_x : 
            start_x, start_y, last_x, last_y = change_points(start_x, start_y, last_x, last_y)
        
        if last_y < start_y :
            distance = (start_y - last_y)
            start_y -= distance
            last_y += distance

        if last_y - start_y < 10 :
            start_y -= 20
            last_y += 20

    area = (start_x, start_y, last_x, last_y)
    crop_img = image.crop(area)

    # if i == 70 :
    #     # image = cv2.line(image, (int(start_x), int(start_y)),(int(start_x), int(start_y)), (255,0,0), 5)
    #     # image = cv2.line(image, (int(last_x), int(last_y)),(int(last_x), int(last_y)), (255,0,0), 5)

    #     # cv2.namedWindow('image')
    #     # cv2.setMouseCallback('image', mouse_callback)
    #     # cv2.imshow("image",image)
    #     # if cv2.waitKey(0) == ord('q'):
    #     #     cv2.destroyAllWindows()  
    #     print(f"s_x : {start_x}, s_y {start_y}, l_x : {last_x}, l_y : {last_y}")
    #     print(area)
    #     print(crop_img.size)
    #     quit()

    try :
        crop_img.save(f"data/V-ST/{image_name}_{i}.jpg")
    except :
        print(crop_img.size)
        print(i)

    # crop_img = cv2.line(image, (start_x, start_y),(start_x, start_y), (255,0,0), 5)
    # crop_img = cv2.line(image, (last_x, last_y),(last_x, last_y), (255,0,0), 5)

    # try :
    #     cv2.imwrite(f"data/{image_name}_{i}.jpg", crop_img)
    # except :
    #     print(f"{image_name}_{i}.jpg")
    #     print(points)
    #     # print(f"s_x : {start_x}, s_y {start_y}, w : {width}, h : {height}")
    #     cv2.imshow("img", crop_img)
    #     quit()

    i += 1

def save_label(image_name, i, label) :
    with open("./gt.txt", "a" ,encoding="UTF-8") as f :
        f.write(f"data/{image_name}_{i}.jpg\t{label}\n")
        f.close()

if __name__ == "__main__" :
    i = 1

    for file in os.listdir(images_path)[37400:44000] :
        if file.find(".json") != -1 :
            print(file)
            with open(images_path + file, "r", encoding="UTF-8") as f :
                image_data = json.load(f)
                for annotation in image_data["annotations"] :
                    bbox = annotation["bbox"]
                    bbox_id = bbox["classid"]
                    if bbox_id == "BIC" or bbox_id == "TYPESIZE" :
                        print(bbox_id)
                        points = bbox["points"]
                        label = bbox["text"]
                        image_name = file.replace(".json","")
                        crop_image_horizontal(points, image_name, bbox_id, i)
                        save_label(image_name, i, label)
                        i += 1