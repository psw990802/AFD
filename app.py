import mysql.connector
from mysql.connector import Error
# 테이블별로 하나씩 주석 해제해서 동작
def create_table():
    try:
        # 데이터베이스에 연결
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="plab",
            database="exampledb"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 테이블 생성 SQL 쿼리 골절 테이블 생성
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS fracture (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_data1 LONGBLOB,
                image_data2 LONGBLOB,
                result VARCHAR(255),
                diagnosis1 TEXT,
                diagnosis2 TEXT,
                audio_data LONGBLOB
            )
            '''
            # 테이블 생성 SQL 쿼리 폐 테이블 생성
            # create_table_query = '''
            # CREATE TABLE IF NOT EXISTS lung (
            #     id INT AUTO_INCREMENT PRIMARY KEY,
            #     image_data1 LONGBLOB,
            #     image_data2 LONGBLOB,
            #     result VARCHAR(255),
            #     diagnosis1 TEXT,
            #     diagnosis2 TEXT,
            #     audio_data LONGBLOB
            # )
            # '''

            # 테이블 생성 SQL 쿼리 개 테이블 생성
            # create_table_query = '''
            # CREATE TABLE IF NOT EXISTS dogbreed (
            #     id INT AUTO_INCREMENT PRIMARY KEY,
            #     image_data1 LONGBLOB,
            #     image_data2 LONGBLOB,
            #     result VARCHAR(255),
            #     diagnosis1 TEXT,
            #     diagnosis2 TEXT,
            #     audio_data LONGBLOB
            # )
            # '''


            # 테이블 생성 실행
            cursor.execute(create_table_query)
            print("dogbreed 테이블이 성공적으로 생성되었습니다.")

    except Error as e:
        print(f"오류 발생: {e}")

    finally:
        # 연결 종료
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL 연결이 종료되었습니다.")

# 테이블 생성 함수 호출
create_table()
