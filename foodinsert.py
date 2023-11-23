import sqlite3

# SQLite3 데이터베이스 연결 (데이터베이스 파일이 없다면 새로 생성됨)
conn = sqlite3.connect('db.sqlite3')

# 커서 생성
cursor = conn.cursor()

# 데이터 삽입 SQL
insert_data_sql = '''
INSERT INTO food (food_name, food_weight, food_carbs, food_proteins, food_fats, food_kcal)
VALUES (?, ?, ?, ?, ?, ?);
'''

# 다수의 데이터 삽입
multiple_data_to_insert = [
    ('blt샌드위치', 220, 18.6, 20.9, 29.6, 423),
    ('건크랜베리', 37, 30.5, 0.5, 0.1, 114),
    ('그라탕', 300, 33, 15, 24, 393),
    ('닭가슴살',200, 0, 46, 2.5, 219),
    ('비빔밥', 400, 89.8, 22.1, 14, 586),
    ('사과', 150, 19.1, 0.4, 0.2, 72),
    ('찐고구마',151, 45.9, 2.6, 0.2, 193),
    ('쌀국수', 244, 16.8, 17.4, 3.9, 176),
    ('연어샐러드',110, 11.8, 12.2, 10.8, 192),
    ('햄샌드위치',220, 8.4, 19, 1, 262)
]

cursor.executemany(insert_data_sql, multiple_data_to_insert)

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()