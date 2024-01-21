import requests
from os import mkdir
import metric_list
import data_sample
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

#인공지능 모니터링용

prometheus_url = "http://192.168.0.12:9090"
data_count = 10
model = load_model('192_168_0_12_RNN.h5')

#데이터 요청
def metric_request(metric_list):
    data_list = []
    for metric_name in metric_list:
        response = requests.get('{0}/api/v1/query'.format(prometheus_url), params={
        'query': metric_name})
        results = response.json()['data']['result']
        data_list.append(results)
    return data_list




data_list = metric_request(metric_list.metrics_list)
subl = []
for results in data_list:
    for result in results:
        subl.append(result["value"][1])

df = pd.DataFrame([subl], columns = rowname.row_name)



df = df.apply(pd.to_numeric, errors='coerce')
scaler = MinMaxScaler(feature_range=(0, 10))
df_scaled = scaler.fit_transform(df.select_dtypes(include=['float64','int64']))

df_scaled = pd.DataFrame(df_scaled, columns=rowname.row_name)
yhat = model.predict(df_scaled)
print(yhat)
