import os
import json
import cv2


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

def get_width(points) :
    x_max = 0
    x_min = 99999999
    max_index = -1
    min_index = -1
    i = 0

    for point in points :
        if point[0] > x_max :
            x_max = point[0]
            max_index = i
        if point[0] < x_min :
            x_min = point[0]
            min_index = i
        i += 1
            
    width = int(points[max_index][0]) - int(points[min_index][0])
    return width

def get_height(points) :
    x_max = 0
    x_min = 99999999
    max_index = -1
    min_index = -1
    i = 0

    for point in points :
        if point[1] > x_max :
            x_max = point[1]
            max_index = i
        if point[1] < x_min :
            x_min = point[1]
            min_index = i
        i += 1
            
    height = int(points[max_index][1]) - int(points[min_index][1])
    return height



def crop_image_horizontal(points, image_name,bbox_id ,i) :
    image = cv2.imread(images_path + image_name + ".jpg")

    first_index = find_first_point(points)

    start_x = int(points[first_index][0])
    start_y = int(points[first_index][1])

    width = get_width(points)
    height = get_height(points)

    # BIC 바운딩박스는 이상하게 밑에 글자도 보여서 TYPESIZE도 보임
    if bbox_id == "BIC" :
        start_x -= 5
        width += 7
        height -= 3

    if i == 63 :
        image = cv2.line(image, (int(points[0][0]), int(points[0][1])),(int(points[0][0]), int(points[0][1])), (255,0,0), 5)
        image = cv2.line(image, (int(points[1][0]), int(points[1][1])),(int(points[1][0]), int(points[1][1])), (255,0,0), 5)
        image = cv2.line(image, (int(points[2][0]), int(points[2][1])),(int(points[2][0]), int(points[2][1])), (255,0,0), 5)
        image = cv2.line(image, (int(points[3][0]), int(points[3][1])),(int(points[3][0]), int(points[3][1])), (255,0,0), 5)

        cv2.imshow("img",image)
        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows()  

    # print(f"s_x : {start_x}, s_y {start_y}, w : {width}, h : {height}")
    crop_img = image[start_y:start_y+height, start_x:start_x+width]

    try :
        cv2.imwrite(f"data/{image_name}_{i}.jpg", crop_img)
    except :
        print(f"{image_name}_{i}.jpg")
        print(points)
        print(f"s_x : {start_x}, s_y {start_y}, w : {width}, h : {height}")
        cv2.imshow("img", crop_img)
        quit()

    i += 1

def save_label(image_name, i, label) :
    with open("./gt.txt", "a" ,encoding="UTF-8") as f :
        f.write(f"data/{image_name}_{i}.jpg\t{label}\n")
        f.close()

i = 1

for file in os.listdir(images_path) :
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

