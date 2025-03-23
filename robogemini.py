from flask import Flask, request, jsonify
from flask_cors import CORS
from roboflow import Roboflow
import os
import mysql.connector
from gtts import gTTS
import base64
import PIL.Image
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
app = Flask(__name__)
CORS(app)
cfname = "config1"
text = ""

roboflow_configs = {
    "config1": {
        "workspace": "capstone-workspace",
        "project": "new-final-dataset-eqnh8",
        "version": 1
    },
    "config2": {
        "workspace": "test-xmfge",
        "project": "test-1-ca75d",
        "version": 2
    },
    "config3": 
        "workspace": "mohammad-amin-asadi-1tacf",
        "project": "bone-fracture-vqdiz",
        "version": 1
    },
    "config4": {
        "workspace": "dog-lee2j",
        "project": "dogs-breeds-lnpqs",
        "version": 1
    }
}
# 업로드할 이미지 저장 경로 설정
UPLOAD_FOLDER = '/home/plab/Desktop/robogemini'  # 경로 변경
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Google API 키 설정
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="plab",
    database="exampledb"
)

# 커서 생성
db_cursor = db_connection.cursor()

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
genai.configure(api_key='your_api_key')
def text_to_speech(text):
    tts = gTTS(text=text, lang='ko', tld='co.kr', slow=False)
    tts.save("/home/plab/Desktop/robogemini/output.mp3")
    #os.system("mpg321 output.mp3")

# MySQL에 데이터 삽입 함수
def insert_data_to_db1(image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data):
    sql = "INSERT INTO dental (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data)
    db_cursor.execute(sql, val)
    db_connection.commit()
def insert_data_to_db2(image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data):
    sql = "INSERT INTO lung (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data)
    db_cursor.execute(sql, val)
    db_connection.commit()
def insert_data_to_db3(image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data):
    sql = "INSERT INTO fracture (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data)
    db_cursor.execute(sql, val)
    db_connection.commit()
def insert_data_to_db4(image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data):
    sql = "INSERT INTO dogbreed (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data)
    db_cursor.execute(sql, val)
    db_connection.commit()
def encode_base64(image_path):
    """
    이미지 파일을 base64로 인코딩하는 함수

    :param image_path: 이미지 파일 경로
    :return: base64로 인코딩된 이미지 문자열
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return encoded_string
  
model2 = genai.GenerativeModel('gemini-1.5-pro')

@app.route('/')
def home():
    return app.send_static_file('index.html')
@app.route('/update_config', methods=['POST'])
def update_config():
    global cfname  # 전역 변수 선언
    data = request.json
    cfname = data.get('config_name', 'config1')  # 기본값은 config1
    print(cfname+"uc")
    return jsonify({'message': f'Config updated to {cfname}'}), 200
# 이미지 업로드 엔드포인트
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    # 파일 저장 경로 지정
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'aimage.jpg')  # 파일 이름 유지
    file.save(save_path)
    
    return jsonify({'message': 'File uploaded successfully'}), 200
@app.route('/gemini-api-endpoint', methods=['POST'])
def gemini_api():
    data = request.get_json()
    global text
    text = data.get('text')
    print("사용자가 입력한 텍스트:", text)
    response = {
        "message": "텍스트 입력이 성공적으로 이루어졌습니다!",
        "input_text": text
    }

    return jsonify(response)
@app.route('/delete_image', methods=['POST'])
def delete_image():
    # 클라이언트에서 POST 요청으로 id를 받아옵니다.
    data = request.get_json()
    image_id = data['id']
    
    try:
        # 데이터베이스에서 해당 ID의 레코드를 삭제합니다.
        if(cfname == 'config1'):
            delete_query = "DELETE FROM dental WHERE id = %s"
        elif(cfname == 'config2'):
            delete_query = "DELETE FROM lung WHERE id = %s"
        elif(cfname == 'config3'):
            delete_query = "DELETE FROM fracture WHERE id = %s"
        elif(cfname == 'config4'):
            delete_query = "DELETE FROM dogbreed WHERE id = %s"
        db_cursor.execute(delete_query, (image_id,))
        db_connection.commit()
        
        return jsonify({"message": "삭제 성공"}), 200
    except mysql.connector.Error as err:
        db_connection.rollback()
        return jsonify({"error": f"삭제 실패: {err}"}), 500
@app.route('/robogemini', methods=['POST'])
def process_image():
    global cfname
    #db_connection = create_db_connection()  # DB 연결
    #config_name = request.form.get('config_name', 'config1')
    config = roboflow_configs.get(cfname, roboflow_configs[cfname])
    rf = Roboflow(api_key=config['api_key'])
    project = rf.workspace(config['workspace']).project(config['project'])
    model = project.version(config['version']).model
    filename = '/home/plab/Desktop/roboflow/aimage.jpg'
    response0 = (model.predict("/home/plab/Desktop/robogemini/aimage.jpg", confidence=25, overlap=30).json())

         # visualize your prediction
    model.predict("/home/plab/Desktop/robogemini/aimage.jpg", confidence=10, overlap=30).save("/home/plab/Desktop/robogemini/prediction.jpg")
    classes = ','.join(prediction['class'] for prediction in response0['predictions'])
    class_confidence_list = [f"[{prediction['class']}, {prediction['confidence'] * 100:.2f}%]" for prediction in response0['predictions']]
    # 컴마로 구분된 문자열로 변환
    result = ','.join(class_confidence_list)
    print(result)
    result = f"질문 : {text}\nResult : {result}"


    image_path = '/home/plab/Desktop/robogemini/aimage.jpg'
    image_path2 = '/home/plab/Desktop/robogemini/prediction.jpg'
    audio_path = "/home/plab/Desktop/robogemini/output.mp3"
    print(f'{filename} 저장됨')
    img1 = PIL.Image.open('/home/plab/Desktop/robogemini/aimage.jpg')
    img2 = PIL.Image.open('/home/plab/Desktop/robogemini/prediction.jpg')
            # Base64로 이미지 인코딩
    encoded_image1 = encode_base64(image_path)        
    encoded_image2 = encode_base64(image_path2)
    # if(cfname == 'config1'):        
    #     response1 = model2.generate_content(["이 사진은 치아를 xray로 촬영한 사진이야. 사진을 보고 질병이 있는지 확인해줘", img1])
    #     response1.resolve()
    #     if(classes == ""):
    #         message23 = "훈련된 모델이 아무 증상도 찾아내지 못했어. 정확하게 찾아낸건지 진단해줘."
    #     else:
    #         message23 = ".훈련된 모델이 " + classes + "를 찾아냈어. 훈련된 모델이 증상을 찾아 바운딩 박스를 그린 사진인데 정확하게 찾아냈는지 진단해줘"
    #     response2 = model2.generate_content([message23, img2])
    #     response2.resolve()
    # elif(cfname == 'config2'):        
    #     response1 = model2.generate_content(["이 사진은 폐를 촬영한 사진이야. 사진을 보고 질병이 있는지 확인해줘", img1])
    #     response1.resolve()
    #     if(classes == ""):
    #         message23 = "훈련된 모델이 아무 증상도 찾아내지 못했어. 정확하게 찾아낸건지 진단해줘."
    #     else:
    #         message23 = ".훈련된 모델이 " + classes + "를 찾아냈어. 훈련된 모델이 품종을 찾아 바운딩 박스를 그린 사진인데 정확하게 찾아냈는지 진단해줘"
    #     response2 = model2.generate_content([message23, img2])
    #     response2.resolve()
    # elif(cfname == 'config3'):        
    #     response1 = model2.generate_content(["이 사진은 뼈를 촬영한 사진이야. 사진을 보고 골절이 있는지 알려줘", img1])
    #     response1.resolve()
    #     if(classes == ""):
    #         message23 = "훈련된 모델이 아무 증상도 찾아내지 못했어. 정확하게 찾아낸건지 진단해줘."
    #     else:
    #         message23 = ".훈련된 모델이 " + classes + "를 찾아냈어. 훈련된 모델이 품종을 찾아 바운딩 박스를 그린 사진인데 정확하게 찾아냈는지 진단해줘"
    #     response2 = model2.generate_content([message23, img2])
    #     response2.resolve()
    # elif(cfname == 'config4'):        
    #     response1 = model2.generate_content(["이 사진은 개를 촬영한 사진이야. 사진을 보고 개에 대한 정보를 알려줘", img1])
    #     response1.resolve()
    #     if(classes == ""):
    #         message23 = "훈련된 모델이 아무 증상도 찾아내지 못했어. 정확하게 찾아낸건지 진단해줘."
    #     else:
    #         message23 = ".훈련된 모델이 " + classes + "를 찾아냈어. 훈련된 모델이 품종을 찾아 바운딩 박스를 그린 사진인데 정확하게 찾아냈는지 진단해줘"
    #     response2 = model2.generate_content([message23, img2])
    #     response2.resolve()
  
    response1 = model2.generate_content([text, img1])
    response1.resolve()
    if(classes == ""):
        message23 = "훈련된 모델이 아무 증상도 찾아내지 못했어. 정확하게 찾아낸건지 진단해줘."
    else:
        message23 = ".훈련된 모델이 " + classes + "를 찾아냈어. 훈련된 모델이 증상을 찾아 바운딩 박스를 그린 사진인데 정확하게 찾아냈는지 진단해줘"
    response2 = model2.generate_content([message23, img2])
    response2.resolve()
    print(response1.text)
    print(response2.text)
            # print(encoded_image)

    text_to_speech(response1.text + response2.text)
    encoded_audio = encode_base64(audio_path)
            # MySQL에 데이터 삽입
    if(cfname == 'config1'): 
        insert_data_to_db1(encoded_image1, encoded_image2, result, response1.text, response2.text, encoded_audio)
    elif(cfname == 'config2'): 
        insert_data_to_db2(encoded_image1, encoded_image2, result, response1.text, response2.text, encoded_audio)
    elif(cfname == 'config3'): 
        insert_data_to_db3(encoded_image1, encoded_image2, result, response1.text, response2.text, encoded_audio)
    elif(cfname == 'config4'): 
        insert_data_to_db4(encoded_image1, encoded_image2, result, response1.text, response2.text, encoded_audio)
    return jsonify({'message': 'File processed successfully'}), 200


@app.route('/get_data', methods=['GET'])
def get_data():
    # config_name = request.form.get('config_name', 'config1')
    global cfname
    if(cfname == 'config1'):
        db_cursor.execute("SELECT * FROM dental")
        print(cfname)
    elif(cfname == 'config2'):
        db_cursor.execute("SELECT * FROM lung")
        print(cfname)
    elif(cfname == 'config3'):
        db_cursor.execute("SELECT * FROM fracture")
        print(cfname)
    elif(cfname == 'config3'):
        db_cursor.execute("SELECT * FROM dogbreed")
        print(cfname)
    rows = db_cursor.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'image_data1': base64.b64encode(row[1]).decode('utf-8') if row[1] else None,
            'image_data2': base64.b64encode(row[2]).decode('utf-8') if row[2] else None,
            'result': row[3],
            'diagnosis1': row[4],
            'diagnosis2': row[5],
            'audio_data': base64.b64encode(row[6]).decode('utf-8') if row[6] else None
        })

    return jsonify(data)
@app.route('/fetch_images', methods=['GET'])
def fetch_images():
    global cfname
    cursor = db_connection.cursor()
    # config_name = request.form.get('config_name', 'config1')
    # 데이터베이스에서 데이터 가져오기
    if(cfname == 'config1'):
        cursor.execute("SELECT id, image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data FROM dental")
        print(cfname)
    elif(cfname == 'config2'):
        cursor.execute("SELECT id, image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data FROM lung")
        print(cfname)
    elif(cfname == 'config3'):
        cursor.execute("SELECT id, image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data FROM fracture")
        print(cfname)
    elif(cfname == 'config4'):
        cursor.execute("SELECT id, image_data1, image_data2, result, diagnosis1, diagnosis2, audio_data FROM dogbreed")
        print(cfname)
    rows = cursor.fetchall()
    
    if not rows:  # 데이터가 없으면
        return jsonify({"success": True, "message": "데이터가 없습니다."})
    images = []
    
    for row in rows:
        image = {
            "id": row[0],
            "image_data1": row[1],
            "image_data2": row[2],
            "result": row[3],
            "diagnosis1": row[4],
            "diagnosis2": row[5],
            "audio_data": row[6]
        }
        images.append(image)

    cursor.close()
    
    response = {
        "success": True,
        "images": images
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765)
