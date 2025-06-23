import os
import http.client
import json
import subprocess


def restart(file):
    if file == "cpp_test":
        os.chdir('docker/cpp_sandbox/')
        subprocess.run(['bash', './restart.sh'], encoding="utf-8")
        os.chdir('../../')
    elif file == "java_test":
        os.chdir('docker/java_sandbox/')
        subprocess.run(['bash', './restart.sh'], encoding="utf-8")    
    else:
        pass


files = ["cpp_test","java_test"]

for file in files:
    data = {
        "dir": f"/{file}/",
        "kb": 100000,
        "args":"",
        "time_limit_in_ms": 10000,
        "stdin_data":"running"
    }

    # 准备请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 创建连接,根据语言不同连接不同的container
    if file == "cpp_test":
        conn = http.client.HTTPConnection("localhost", 8001)
    elif file == "java_test":
        conn = http.client.HTTPConnection("localhost", 8002)
    elif file == "others":
        pass

    # 将数据转换为JSON格式
    json_data = json.dumps(data)

    # 发送POST请求
    try:
        conn.request("POST", "/sandbox/", json_data, headers)
        response = conn.getresponse()
        body = response.read()
        status_code = response.status
        json_data =  json.loads(body.decode("utf-8"))
    except:
        restart(file)
        continue
           
    finally:
        conn.close()
    #检验输出
    if status_code != 200:
        restart(file)
        continue
    if json_data["Status"] != "0":
        restart(file)
        continue
    elif json_data["Output"].strip() != "running":
        restart(file)
        continue
    else:
        print(f"{file} success")