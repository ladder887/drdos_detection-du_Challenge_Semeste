import metric_list
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import seaborn as sns
import requests
#import imblearn
from sklearn.neighbors import LocalOutlierFactor
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras
from sklearn.metrics import classification_report, confusion_matrix
# Ignore warnings
import warnings
import time
import socket
import json
warnings.filterwarnings('ignore')

#정상 1 공격 0

my_ip = "192.168.0.15"                       #설정
send_ip = ""                                 #설정
prometheus_url = "http://192.168.0.15:9090"  #설정

plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

test = pd.read_csv('192_168_0_15_total.csv')   #설정
test = test.drop(['timestamp'], axis=1)
test = test.drop(['Label'], axis=1)
test.head()

model = keras.models.load_model('192_168_0_15_RNN.h5')   #설정
scaler = MinMaxScaler(feature_range=(0, 10))



#데이터 요청 함수
def metric_request(metric_list):
    data_list = []
    for metric_name in metric_list:
        response = requests.get('{0}/api/v1/query'.format(prometheus_url), params={
        'query': metric_name})
        results = response.json()['data']['result']
        for result in results:
            data_list.append(result["value"][1])
    return data_list

#인공지능 탐지
def detection(test):
    #마지막 행의 데이터 갱신
    test.iloc[-1] = metric_request(metric_list.metrics_list)

    #데이터 전처리
    test = test.apply(pd.to_numeric, errors='coerce')
    cols = test.select_dtypes(include=['float64','int64']).columns
    sc_test = scaler.fit_transform(test.select_dtypes(include=['float64','int64']))
    testX = pd.DataFrame(sc_test, columns = cols)
    testX.head()

    #마지막 행만 추출
    testX = testX.iloc[-1:]

    Y_pred = model.predict(testX)

    y_pred = np.argmax(Y_pred, axis=1)

    y_pred = model.predict(testX)

    predict_classes=int(np.argmax(y_pred,axis=1)[0])

    #print(predict_classes)
    return predict_classes

#소켓
def send_data(value):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (send_ip, 9999)
        sock.connect(server_address)
        joon_data = json.dumps(value)
    
        sock.sendall(json_data.encode())

        sock.close()
    except:
        print("err")

while True:
    predict_classes = detection(test)
    value = {"IP" : my_ip, "result" : predict_classes}
    send_data(value)
    print(value)
    time.sleep(3)