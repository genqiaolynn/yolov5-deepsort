from objdetector import Detector
import imutils
import cv2, math
import numpy as np
VIDEO_PATH = './video/test_person.mp4'
# VIDEO_PATH = 'output_file.mp4'
RESULT_PATH = 'result2.mp4'
######################


def draw_boxes(img, bbox, identities=None, offset=(50, 50), color=(255,0,0), distance=1.00,speed=1.00):

    for i, box in enumerate(bbox):
        x1, y1, x2, y2, _, cf = [i for i in box]
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)

        distance = float(distance)  # 使用 numpy 创建一个浮点数
        text1 = "distance: {:.2f} m".format((distance))
        text2 = "speed: {:.1f}   km/h".format((speed))
        ##########
        #text = "dis: {.2f}".format(distance)
        #########

        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        # box text and bar
        #id = int(identities[i]) if identities is not None else 0
        color =(0,0,255)
        label1 = "Distance"
        cv2.putText(img, text2, (x1, y1 + 54), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 6)
        cv2.putText(img, text1, (x1, y1 +14), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 6)  # 修改 2,.,2
    return img


def calculate_velocity(x1, y1, x2, y2, n, delta_t):
    distance1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    time = n * delta_t
    velocity = distance1 / time
    return velocity


def calculate_distance(actual_height, actual_width, triangle_height, triangle_width, focal_length):
    distance = (actual_height * focal_length) / triangle_height
    return distance


def main():

    func_status = {}
    func_status['headpose'] = None

    name = 'demo'

    det = Detector()
    cap = cv2.VideoCapture(VIDEO_PATH)
    fps = int(cap.get(5))
    print('fps:', fps)
    t = int(1000/fps)

    size = None
    videoWriter = None

    while True:

        # try:
        _, im = cap.read()
        if im is None:
            break

        result1 = det.feedCap(im, func_status)
        result = result1['frame']
        #object1 = result['list_of_ids']
        boxes=result1['obj_bboxes']
#########################################
        curr_x=0
        curr_y=0

        if boxes:
            print("-----------",boxes)
            print('------------type:',type(boxes))
            for l in range(len(boxes)):
                x1, y1, x2, y2, lbl, conf=boxes[l][0],boxes[l][1],boxes[l][2],boxes[l][3],boxes[l][4],boxes[l][5]
                result_speed = calculate_velocity(curr_x, curr_y, x2, y2, 1, 0.5)/3.6
                curr_x=x1
                curr_y =y1

                print("速度：", result_speed)
                actual_height=20
                actual_width=100
                triangle_height=y2-y1
                triangle_width=x2-x1
                focal_length=10
                distance = calculate_distance(actual_height, actual_width, triangle_height, triangle_width, focal_length)
                print("di----------s", type(distance))
                if distance <10 and result_speed>10:
                    color=(0,255,255)
                result = draw_boxes(result, boxes, identities=None, offset=(0, 0), color=color,distance=distance,speed=result_speed)

        else:
            color=(255,0,0)
##################################################
        result=draw_boxes(result, boxes, identities=None, offset=(0, 0),color=color)

        result = imutils.resize(result, height=500)
        if videoWriter is None:
            fourcc = cv2.VideoWriter_fourcc(
                'm', 'p', '4', 'v')  # opencv3.0
            videoWriter = cv2.VideoWriter(
                RESULT_PATH, fourcc, fps, (result.shape[1], result.shape[0]))

        videoWriter.write(result)
        cv2.imshow(name, result)
        cv2.waitKey(t)

        if cv2.getWindowProperty(name, cv2.WND_PROP_AUTOSIZE) < 1:
            # 点x退出
            break

    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()