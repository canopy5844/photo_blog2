import os
import cv2
import pathlib
import requests
from datetime import datetime

class ChangeDetection:
    result_prev = []
    HOST = 'http://127.0.0.1:8000'
    username = 'apple'
    password = 't7gr@*e5'
    # HOST = 'https://thinking.pythonanywhere.com'
    # username = 'user1'
    # password = 'i%w7p5#6'
    token = ''
    title = ''
    text = ''
    threshold = 0.0
    def __init__(self, names):
        self.result_prev = [0 for i in range(len(names))]
        res = requests.post(self.HOST + '/api-token-auth/', {
            'username': self.username,
            'password': self.password,
        })
        res.raise_for_status()
        self.token = res.json()['token']
        print(self.token)
    
    def add(self, names, detected_current, confidence, max_confidence_crop, save_crop: bool, save_dir, image):
        self.title = ''
        self.text = ''
        change_flag = 0 #변화 감지 플레그
        i = 0
        while i < len(self.result_prev):
            if self.result_prev[i]==0 and detected_current[i]==1 :
                change_flag = 1
                self.title = names[i]
                self.text += names[i] + ", "
            i += 1
        
        if self.text.endswith(', '):
            self.text = self.text[:-2]
            
        max_confidence = 0.0
        if len(confidence) > 0:
            max_confidence = max(confidence.values())
        gt_threshold = max_confidence >= self.threshold
        
            
        self.result_prev = detected_current[:] # 객체 검출 상태 저장
        if change_flag == 1:
            if save_crop and max_confidence_crop is not None:
                self.send(gt_threshold, save_dir, max_confidence_crop[0])
            else:
                self.send(gt_threshold, save_dir, image)

    def send(self, gt, save_dir, image):
        now = datetime.now()
        now.isoformat()
        today = datetime.now()
        save_path = os.getcwd() / save_dir / 'detected' / str(today.year) / str(today.month) / str(today.day)
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)
        full_path = save_path / '{0}-{1}-{2}-{3}.jpg'.format(today.hour,today.minute,today.second,today.microsecond)
        dst = cv2.resize(image, dsize=(320, 240), interpolation=cv2.INTER_AREA)
        if not gt:
            dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(full_path, dst)
        # 인증이 필요한 요청에 아래의 headers를 붙임
        headers = {'Authorization' : 'Token ' + self.token, 'Accept' : 'application/json'}
        # Post Create
        data = {
            'title' : self.title,
            'text' : self.text,
            'created_date' : now,
            'published_date' : now
        }
        file = {'image' : open(full_path, 'rb')}
        res = requests.post(self.HOST + '/api_root/Post/', data=data, files=file, headers=headers)
        print(res)