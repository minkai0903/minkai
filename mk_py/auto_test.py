
import sys
import json
import requests
import os
import shutil
import logging  #日志模块
from PIL import Image, ImageDraw, ImageFont  #图像处理模块
import base64
import datetime
import multiprocessing #进程模块
import threading  #线程模块
from optparse import OptionParser #用来为脚本传递命令参数，采用预先定义好的选项来解析命令行参数
import time
import importlib

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    importlib.reload(sys)
    sys.setdefaultencoding(defaultencoding)

def get_json_msg(json_file):
    with open(json_file) as f:
        text = f.read()
        json_msg = json.loads(text, encoding='utf-8')
    return json_msg

def get_files(src_dir, typeid):
    filelist = []
    for dir, sdir, files in os.walk(src_dir):
        if not files:
            continue
        for file in files:
            filelist.append(os.path.join(dir,file))
    if typeid == 0:
        jsonlist = [i for i in filelist if i.lower().endswith('.json')]
        return jsonlist
    if typeid == 1:
        imglist = [i for i in filelist if i.lower().endswith('.jpg')]
        return imglist


def json_get_orig_images(src_dir, dst_dir):
    jsonlist = get_files(src_dir, 0)
    for jsonfile in jsonlist:
        new_dir = dst_dir + jsonfile.split('/')[-2] 
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        json_msg = get_json_msg(jsonfile)
        image_file = json_msg.get('image_path')
        image_id = json_msg.get('image_id')
        new_name = str(image_id) + '_' + os.path.basename(image_file)
        localimage = os.path.join(new_dir ,new_name)
        shutil.copy(image_file, localimage)

def change_name(src_dir, dst_dir):
    imagelist = get_files(src_dir, 1)
    for img in imagelist:
        new_dir = dst_dir + img.split('/')[-2] 
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        if img.split('/')[-2] in ["1092", "1093"]:
            basename = os.path.basename(img).split('_')
            new_name = '1_' + basename[0] + '_' + basename[2] + '.jpg'
        if img.split('/')[-2] in ["1102", "1290"] :
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[-1]
        if img.split('/')[-2] in ["1108", "1109", "1122", "1123", "1124", "1125"] :
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[4] + '.jpg'
        if img.split('/')[-2] in ["1258"] :
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[-1].split('@')[3] + '.jpg'
        if img.split('/')[-2] in ["1261"]:
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[-2] + '.jpg'
        if img.split('/')[-2] in ["1286"]:
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[-3] + '.jpg'
        if img.split('/')[-2] in ["1288", "1470"]:
            basename = os.path.basename(img).split('_')
            new_name = '4_' + basename[0] + '_' + basename[5] + '.jpg'
        localimage = os.path.join(new_dir, new_name)
        shutil.copy(img, localimage)



def split_image(img_path, out_dir, mode):
    img = Image.open(img_path);img.load()   
    [w, h] = img.size
    filename = os.path.basename(img_path).strip(".jpg") 
    if mode=="2x2":
        splited_img1 = img.crop([0, 0, w/2-1, h/2-1])
        splited_img2 = img.crop([w/2, 0, w-1, h/2-1])
        splited_img3 = img.crop([0, h/2, w/2-1, h-1])
        splited_img4 = img.crop([w/2, h/2, w-1, h-1])
        
        if os.path.basename(img_path).split('_')[0] in '4':

            splited_img1_path = "%s/%s_1.jpg"%(out_dir, filename) 
            splited_img2_path = "%s/%s_2.jpg"%(out_dir, filename) 
            splited_img3_path = "%s/%s_3.jpg"%(out_dir, filename) 
            splited_img4_path = "%s/%s_4.jpg"%(out_dir, filename) 
            splited_img1.save(splited_img1_path)
            splited_img2.save(splited_img2_path)
            splited_img3.save(splited_img3_path)
            splited_img4.save(splited_img4_path)
 
        if os.path.basename(img_path).split('_')[0] in '1':

            splited_img1_path = "%s/%s_4.jpg"%(out_dir, filename) 
            splited_img2_path = "%s/%s_1.jpg"%(out_dir, filename) 
            splited_img3_path = "%s/%s_2.jpg"%(out_dir, filename) 
            splited_img4_path = "%s/%s_3.jpg"%(out_dir, filename) 
 
            splited_img1.save(splited_img1_path)
            splited_img2.save(splited_img2_path)
            splited_img3.save(splited_img3_path)
            splited_img4.save(splited_img4_path)
        return [splited_img1_path, splited_img2_path, splited_img3_path,splited_img4_path]

    elif mode=="1x2":
        splited_img1 = img.crop([0, 0, w/2, h-1])
        splited_img2 = img.crop([w/2, 0, w-1, h-1])

        splited_img1_path = "%s/%s_1.jpg"%(out_dir, filename) 
        splited_img2_path = "%s/%s_2.jpg"%(out_dir, filename) 
 
        splited_img1.save(splited_img1_path)
        splited_img2.save(splited_img2_path)
        return [splited_img1_path, splited_img2_path]

    elif mode=="1x3":
        splited_img1 = img.crop([0, 0, w/3-1, h-1])
        splited_img2 = img.crop([w/3, 0, 2*w/3-1, h-1])
        splited_img3 = img.crop([2*w/3, 0, w-1, h-1])

        splited_img1_path = "%s/%s_1.jpg"%(out_dir, filename) 
        splited_img2_path = "%s/%s_2.jpg"%(out_dir, filename) 
        splited_img3_path = "%s/%s_3.jpg"%(out_dir, filename) 

        splited_img1.save(splited_img1_path)
        splited_img2.save(splited_img2_path)
        splited_img3.save(splited_img3_path)
        return [splited_img1_path, splited_img2_path, splited_img3_path]
    elif mode=="3x1":
        splited_img1 = img.crop([0, 0, w-1, h/3-1])
        splited_img2 = img.crop([0, h/3, w-1, 2*h/3-1])
        splited_img3 = img.crop([0, 2*h/3, w-1, h-1])

        splited_img1_path = "%s/%s_1.jpg"%(out_dir, filename) 
        splited_img2_path = "%s/%s_2.jpg"%(out_dir, filename) 
        splited_img3_path = "%s/%s_3.jpg"%(out_dir, filename) 

        splited_img1.save(splited_img1_path)
        splited_img2.save(splited_img2_path)
        splited_img3.save(splited_img3_path)
        return [splited_img1_path, splited_img2_path, splited_img3_path]
 
    elif mode == "1x1":
        splited_img1_path = "%s/%s_1.jpg"%(out_dir, filename) 
        img.save(splited_img1_path)
        return [splited_img1_path]


calc_param_patern = """
{{
    "Detect": {{
        "IsDet": true,
        "Mode": {mode}
    }},
    "Recognize": {{
        "Person": {{
            "IsRec": {Person}
            }},
        "Feature": {{
            "IsRec": {Feature} 
        }},
        "Vehicle": {{
            "Rack": {{
                "IsRec":{Rack} 
            }},
            "Sunroof": {{
                "IsRec": {Sunroof}
            }},
            "SpareTire": {{
                "IsRec": {SpareTire} 
            }},
            "Belt": {{
                "IsRec": {Belt}
            }},
            "Crash": {{
                "IsRec":{Crash}
            }},
            "Brand": {{
                "IsRec": {Brand}
            }},
            "Color": {{
                "IsRec": {Color}
            }},
            "Call": {{
                "IsRec": {Call}
            }},
            "Type": {{
                "IsRec": {Type}
            }},
            "Danger": {{
                "IsRec": {Danger}
            }},
            "Plate": {{
                "IsRec": {Plate}
            }},
            "Marker": {{
                "IsRec": {Marker} 
            }},
            "Slag": {{
                "IsRec": {Slag} 
            }},
            "Convertible": {{
                "IsRec" : {Convertible} 
            }},
            "Manned":{{
                "IsRec" : {Manned}                         
            }},
            "ModelingPoints":{{
                "IsRec" : {ModelingPoints}                         
            }},
            "Violation":{{
                "IsRec" : {Violation}
            }}
        }}
    }}
}}

"""

color = (255, 255, 0)
#font_path = "%s/fonts"%os.environ["RES_PATH"]
font_path = "./picture"
font_small = ImageFont.truetype('%s/ukai.ttc'%font_path, 16)
font = ImageFont.truetype('%s/ukai.ttc'%font_path, 20)
font_big = ImageFont.truetype('%s/ukai.ttc'%font_path, 40)

def draw_rect_with_texts(draw, xywh_rect, texts, top=True, color=color, font=font):
    x, y, w, h = xywh_rect
    draw.rectangle([x, y, x+w, y+h], outline=color)
    if not texts:
        return
    (x, y) = (x, y) if top else (x, y+h)
    for text in texts:
        if not text:
            continue
        draw.text((x,y), str(text), fill=color, font=font)
        y = y + font.getsize("中")[0]

def get_calcparam_by_property(mode):
    property_map = {"mode":0,"Person":"false","Feature":"false","Rack":"false","Sunroof":"false","SpareTire":"false","Belt":"false","Crash":"false","Brand":"false","Color":"false","Call":"false","Type":"false","Danger":"false","Plate":"false","Marker":"false","Slag":"false","Convertible":"false","Manned":"false","ModelingPoints":"false","Violation":"false"}
    property_map["mode"]=mode
    calc_param = calc_param_patern.format(**property_map)
    calc_param_dict = json.loads(calc_param)
    return calc_param_dict

def recog_images(image_list, mode, url):
    image_datas = []
    for image_path in image_list:
        assert os.path.exists(image_path)
        with open(image_path, 'rb') as fimg:
            fsize = os.path.getsize(image_path)
            image_data = fimg.read(fsize)
        image_datas.append(base64.b64encode(image_data))
    calc_param_dict = get_calcparam_by_property(mode)
    calc_param_dict["Recognize"]["ObjLocations"]=[]

    calc_param = json.dumps(calc_param_dict)
    post_data = json.dumps(dict(
                calc_param = calc_param,
                images = image_datas))
    rst_json = None
    for i in range(3):
        try:
            rsp = requests.post(url, post_data)
            #logging.info("rsp="+rsp.content)
            rst_json = json.loads(rsp.content)
            break
        except Exception as ex:
            logging.warn("post or load exception:"+str(ex))
            continue
    assert rst_json is not  None
    return rst_json


def get_car_rect(image_list, url):  #识别检测全图车辆坐标
    rst_json = recog_images(image_list, 1, url)
    img = Image.open(image_list[0]);img.load()   
    [w, h] = img.size
    rect_list = []
    
    imageResult1 = rst_json.get('ImageResults')[0]
    if imageResult1.get('Code') != 0:
        print("imges[0] is no car")
    for car in imageResult1.get('Vehicles'):
        if car.get('Detect').get('Code') != 0:
            continue
        if car.get('Detect').get('Car'):
            car_rect  = car.get('Detect').get('Car').get('Rect')
            rect_list.append(car_rect)

    imageResult2 = rst_json.get('ImageResults')[1]
    if imageResult2.get('Code') != 0:
        print("imges[1] is no car")
    for car in imageResult2.get('Vehicles'):
        if car.get('Detect').get('Code') != 0:
            continue
        if car.get('Detect').get('Car'):
            car_rect  = car.get('Detect').get('Car').get('Rect')
            rect_list.append([car_rect[0]+w,car_rect[1],car_rect[2],car_rect[3]])
    
    imageResult3 = rst_json.get('ImageResults')[2]
    if imageResult3.get('Code') != 0:
        print("imges[2] is no car")
    for car in imageResult3.get('Vehicles'):
        if car.get('Detect').get('Code') != 0:
            continue
        if car.get('Detect').get('Car'):
            car_rect  = car.get('Detect').get('Car').get('Rect')
            rect_list.append([car_rect[0],car_rect[1]+h,car_rect[2],car_rect[3]])
    
    imageResult4 = rst_json.get('ImageResults')[3]
    if imageResult4.get('Code') != 0:
        print("imges[3] is no car")
    for car in imageResult4.get('Vehicles'):
        if car.get('Detect').get('Code') != 0:
            continue
        if car.get('Detect').get('Car'):
            car_rect  = car.get('Detect').get('Car').get('Rect')
            rect_list.append([car_rect[0]+w,car_rect[1]+h,car_rect[2],car_rect[3]])
    
    return rect_list

def get_json_dict(src_dir):
    jsonlist = get_files(src_dir, 0)
    msg_list = {}
    for json_msg in jsonlist:
        jsonname = os.path.basename(json_msg).split('.json')[0]
        with open(json_msg, 'r') as f:
            line = json.load(f)
        msg_list[jsonname] = line
    return msg_list


def find_main_guid(car_msg):
    guid_w = {}
    w_list = []
    for car in car_msg.get('cars'):
        car_w = int(car.get('car_body').split(',')[2])
        w_list.append(car_w)
        guid_w[car_w] = car.get('guid') 
    main_guid = guid_w[max(w_list)]
    return main_guid


def get_markinfo(car_msg):
    all_rect_list = []
    main_car_rect = []
    
    if len(car_msg.get('cars')) <= 4:
        for car in car_msg.get('cars'):
            carrect = car.get('car_body').split(',')
            rect = [int(carrect[0]),int(carrect[1]),int(carrect[2]),int(carrect[3])]
            main_car_rect.append(rect)
        all_rect_list = main_car_rect
        return all_rect_list , main_car_rect
    
    main_guid = find_main_guid(car_msg)

    for car in car_msg.get('cars'):
        if car.get('guid') != main_guid:
            continue
        carrect = car.get('car_body').split(',')
        rect = [int(carrect[0]),int(carrect[1]),int(carrect[2]),int(carrect[3])]
        main_car_rect.append(rect)

    return all_rect_list , main_car_rect


def check_iou(rect_src, rect_dst):
    [x1,y1,w1,h1] = rect_src
    x2 = x1 + w1
    y2 = y1 + h1
    [x3,y3,w2,h2] = rect_dst
    x4 = x3 + w2
    y4 = y3 + h2
    iou_w = min(x1,x2,x3,x4) + w1 + w2 - max(x1,x2,x3,x4)
    iou_h = min(y1,y2,y3,y4) + h1 + h2 - max(y1,y2,y3,y4)
    if iou_w < 0 or  iou_h < 0:
        return False
    iou = float(iou_w*iou_h)/(w2*h2)
    return iou
    

def check_detect(all_mark_list, image_rect_list,draw):
    mark_num = len(all_mark_list)
    picknum = 0
    for all_mark in all_mark_list:
        for image_rect in image_rect_list:
            iou = check_iou(image_rect, all_mark)
            if iou and iou > 0.8:
                #draw_rect_with_texts(draw,image_rect,[])
                picknum += 1
                break
    return picknum , mark_num


def check_recog(recog_rect_list, all_mark_list, draw):
    recog_num = len(recog_rect_list)
    if recog_num == 0:
        return 0, 0
    picknum = 0
    for recog_rect in recog_rect_list:
        for car_mark in all_mark_list:
            iou = check_iou(car_mark, recog_rect)
            if iou and iou > 0.8:
                draw_rect_with_texts(draw,recog_rect,[])
                picknum += 1
                break
    if picknum == recog_num:
        return 1, 1
    else:
        return 0, 1

def merge_into_group(image_list):
    group = {}
    for image_path in image_list:
       filename = os.path.basename(image_path)
       tokens = filename.split("_")
       prefix = "".join(tokens[0:-1])
       if not group.has_key(prefix):
            group[prefix] = []
       group[prefix].append(image_path)
    return group.values()


def post_nomalrecog(imagelist, detect_url):
    post_data = {}
    grouped_image = {}
    post_data["violation_type"] = ["9000"]
    post_data["camera_type"] = 0
    imglist = merge_into_group(imagelist)[0]
    serial_images = [] 
    for image_path in imglist[:-1]: 
        with open(image_path, 'rb') as fimg:
            fsize = os.path.getsize(image_path)
            image_data = fimg.read(fsize)
        serial_images.append(base64.b64encode(image_data))
    post_data["grouped_image"] = grouped_image 
    grouped_image["serial_images"] = serial_images
    with open(imglist[-1], 'rb') as f:
        fsize = os.path.getsize(imglist[-1])
        img_data = f.read(fsize) 
        grouped_image['feature_image'] = base64.b64encode(img_data)
    post_data['license'] = os.path.basename(imglist[0]).split('_')[2] 
    post_data['image_attr'] = None
    url = detect_url
    #json.dump(post_data,file("a.json","w"),indent=4,ensure_ascii= False)
    post_recog_data = json.dumps(post_data)
    try:
        rsp = requests.post(url, post_recog_data)
        #logging.info("rsp="+rsp.content)
        rst_json = json.loads(rsp.content)
    except Exception as ex:
        logging.warn("post or load exception:"+str(ex))
        return rst_json
    return rst_json


def get_json_rect(image,msg_list):  #识别标注的车辆坐标
    json_name = os.path.basename(image).split('_')[1] 
    pick_json = msg_list.get(json_name)
    all_mark_list , car_mark_list = get_markinfo(pick_json)
    return car_mark_list

def get_recog_rect(image_list, detect_url):  #识别车辆坐标
    img = Image.open(image_list[0]);img.load()   
    [w, h] = img.size
    recog_json  = post_nomalrecog(image_list, detect_url)
    recog_rect_list = []
    if recog_json.get('code') != 0:
        return []
    car_results = recog_json.get('violation_results').get('9000').get('car_results')[0].get('recog_info')
    car_rect1 = car_results.get('car_rect')[0]
    car_rect2 = car_results.get('car_rect')[1]
    car_rect3 = car_results.get('car_rect')[2]
    if car_rect1 is not None:
        recog_rect_list.append(car_rect1.get('Rect'))
    if car_rect2 is not None:
        rect2 = car_rect2.get('Rect')
        rect2[0] += w
        recog_rect_list.append(rect2)
    if car_rect3 is not None:
        rect3 = car_rect3.get('Rect')
        rect3[1] += h
        recog_rect_list.append(rect3)
    return recog_rect_list


def test_process(queue, stop_semp, dst_dir, save_dir, msg_list, url, detect_url):
    while(True):
        try:
            logging.info("req_queue size is %d before get"%queue.qsize())
            image = queue.get(True, 1) 
        except Exception as ex:
           if (stop_semp.value == True):
               logging.info("stop signal got")
               break
           else:
               logging.info("get image exception:"+str(ex))
               time.sleep(1)
               continue
        single_image_list = split_image(image, dst_dir, "2x2")
#获取匹配识别车辆坐标信息
        recog_rect_list = get_recog_rect(single_image_list, detect_url)
#获取检测全图车辆坐标信息
        image_rect_list = get_car_rect(single_image_list, url)
#获取标注的车辆坐标信息
        car_mark_list = get_json_rect(image,msg_list)

        img = Image.open(image);img.load()
        draw = ImageDraw.Draw(img)
        detect_num, mark_num = check_detect(car_mark_list, image_rect_list,draw) 
        recog_num, img_num  = check_recog(recog_rect_list, car_mark_list, draw) 
        global detect_match
        global detect_nums
        global recog_match
        global recog_nums
        detect_match += detect_num
        detect_nums += mark_num
        recog_match += recog_num
        recog_nums += img_num
        img.save("%s/%s"%(save_dir, os.path.basename(image)))
            

def main():
    logging.basicConfig(level=logging.INFO,   #配置日志
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    filename='auto_test_match.log',
                    filemode='w')
    parser = OptionParser()
    parser.add_option('-i', '--image_dir', help="the dir of test image files", default='./normal_images/1124')
    parser.add_option('-j', '--json_dir',  help="json dir", default='/mnt/mfs3/zhangshuai/预审测试集2')
    parser.add_option('-s', '--server', help="ip:port of the testing server", default="http://192.168.1.181:38182/recog/")
    parser.add_option('-o', '--output', help="the output dir", default="result")
    parser.add_option('-t', '--thread_num', type=int, help="thread num", default=20)
    options, args = parser.parse_args()
    image_dir = options.image_dir or '../images'
    test_url = options.server
    detect_url = "http://192.168.1.181:21345/recog_violation/"

    if os.path.exists(options.output):
        os.system("rm %s -rf" % options.output)
    dst_dir = options.output + '/split_images/'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    save_dir = options.output + '/draw_images/' 
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    print(datetime.datetime.now())
    json_dir = options.json_dir
    msg_list = get_json_dict(json_dir)
    global detect_match
    global detect_nums
    global recog_match
    global recog_nums
    detect_match = 0.0
    detect_nums = 1
    recog_match = 0.0
    recog_nums = 1
    
    queue = multiprocessing.Queue(100)  #多进程
    stop_semp = multiprocessing.Value('b', False)
    thread_list = []

    for i in range(options.thread_num): #启动线程
        process = threading.Thread(target=test_process, args = (queue, stop_semp, dst_dir, save_dir, msg_list, test_url, detect_url))
        process.start()
        thread_list.append(process)

    print(datetime.datetime.now())
    imagelist = get_files(image_dir, 1)
    for image in imagelist:
        queue.put(image)
            
    stop_semp.value = True
    for thread in thread_list:
        thread.join()
    print(detect_match, recog_match)
    print(detect_match/detect_nums)
    print(recog_match/recog_nums)

if __name__ == '__main__':
    main()

