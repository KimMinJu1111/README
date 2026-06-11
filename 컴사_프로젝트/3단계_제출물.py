# bmi 계산하는 함수
def calculate_bmi(height, weight):
    height_m = height/100    # cm로 입력받은 키를 m로 변환
    bmi = round(weight / (height_m**2), 2)    # bmi 계산
    return bmi    # 계산한 bmi 반환

# 사용자에게 건강상태 입력받는 함수(이름, 키, 몸무게, 수축기혈압, 이완기혈압, 공복혈당)
'''def health_input():
    while True:
        try:
            name = input('이름 : ')
            height = float(input('키(cm) : '))
            weight = float(input('몸무게(kg) : '))
            bp_systolic = int(input('수축기혈압 : '))
            bp_diastolic = int(input('이완기혈압 : '))
            glucose = int(input('공복혈당 : '))

            if height <= 0:
                print('키는 0보다 큰 숫자로 입력하세요.')
                continue

            if weight <= 0:
                print('몸무게는 0보다 큰 숫자로 입력하세요.')
                continue

            if bp_systolic <= 0 or bp_diastolic <= 0:
                print('혈압은 0보다 큰 숫자로 입력하세요.')
                continue

            if glucose <= 0:
                print('공복혈당은 0보다 큰 숫자로 입력하세요.')
                continue

            return name, height, weight, bp_systolic, bp_diastolic, glucose

        except ValueError:
            print('키, 몸무게, 혈압, 공복혈당은 숫자로 입력하세요.')'''

# 사용자에게 값 입력받을 때 정확한 값 입력받도록 하는 함수 (AI 도움)
def input_number(message, number_type):
    while True:
        try:
            value = number_type(input(message))

            if value <= 0:
                print('0보다 큰 숫자로 입력하세요.')
                continue

            return value

        except ValueError:
            print('숫자로 입력하세요.')

# 사용자에게 건강상태 입력받는 함수(이름, 키, 몸무게, 수축기혈압, 이완기혈압, 공복혈당)
def health_input():
    name = input('이름 : ')

    height = input_number('키(cm) : ', float)
    weight = input_number('몸무게(kg) : ', float)
    bp_systolic = input_number('수축기혈압 : ', int)
    bp_diastolic = input_number('이완기혈압 : ', int)
    glucose = input_number('공복혈당 : ', int)

    return name, height, weight, bp_systolic, bp_diastolic, glucose


# 사용자에게 성별, 나이 입력받는 함수
def gender_age_input():
    # 성별 입력
    while True:
        try:
            gender = int(input('남자 = 1 / 여자 = 2 : '))

            if gender != 1 and gender != 2:
                print('성별은 1 또는 2만 입력하세요.')
                continue

            break

        except ValueError:
            print('숫자만 입력하세요.')

    # 나이 입력
    while True:
        try:
            age = int(input('나이 : '))

            if age < 0:
                print('나이는 0 이상으로 입력하세요.')
                continue

            break

        except ValueError:
            print('숫자만 입력하세요.')

    # 나이를 5세 단위 연령대 코드로 변환
    if age >= 85:
        age_group = 18
    else:
        age_group = (age // 5) + 1

    return gender, age_group

# 1-1) BMI 판별하는 함수
def classify_bmi(bmi):
    if bmi < 18.5:
        result_bmi = '저체중'    # bmi가 18.5 미만이면 '저체중'
    elif bmi < 23:
        result_bmi = '정상'    # bmi가 23 미만이면 '정상'
    elif bmi < 25:
        result_bmi = '과체중'    # bmi가 25 미만이면 '과체중'
    else:
        result_bmi = '비만'     # 그 외 '비만'
    return result_bmi           # bmi 결과 반환

# 1-2) 혈압 판별하는 함수
def classify_bp(bp_systolic, bp_diastolic):
    if bp_systolic >= 140 or bp_diastolic >= 90:
        result_bp = '고혈압'    # 수축기 혈압이 140 이상이거나, 이완기 혈압이 90 이상이면 '고혈압'
    elif bp_systolic < 90 or bp_diastolic < 60:
        result_bp = '저혈압'    # 수축기혈압이 90 미만이거나, 이완기 혈압이 60 미만이면 '저혈압'
    elif bp_systolic < 120 and bp_diastolic < 80:
        result_bp = '정상'      # 수축기 혈압이 120 미만이고, 이완기 혈압이 80 미만이면 '정상'
    else:
        result_bp = '주의 혈압' # 그 외 '주의 혈압'
    return result_bp            # 혈압 결과 반환

# 1-3) 혈당 판별하는 함수
def classify_glucose(glucose):
    if glucose < 100:
        result_glucose = '정상'    # 공복혈당이 100 미만이면 '정상'
    elif glucose < 126:
        result_glucose = '공복혈당장애' # 공복혈당이 126 미만이면 '공복혈당장애'
    else:
        result_glucose = '당뇨병'      # 공복혈당이 126 이상이면 '당뇨병'
    return result_glucose           # 혈당 결과 반환

# 크기 비교해서 문장 출력하는 함수 (집단 평균과 비교할 때 사용)
def compare_value(name, item_name, user_value, avg_value):
    difference = abs(user_value - avg_value)

    if user_value < avg_value:
        return f'{name}님의 {item_name}은 평균보다 {difference:.1f} 만큼 낮습니다.'
    elif user_value > avg_value:
        return f'{name}님의 {item_name}은 평균보다 {difference:.1f} 만큼 높습니다.'
    else:
        return f'{name}님의 {item_name}은 평균과 같습니다.'

# 2) 집단 평균 계산하고 사용자 건강수치와 비교하는 함수
def compare_average(user_data, bmi, filtered_data):

    # 같은 성별, 연령 집단이 없을 때 (추가)   
    if len(filtered_data) == 0:             
        return '비교할 데이터가 없습니다.'

    avg_bmi = sum(calculate_bmi(data['height'], data['weight']) for data in filtered_data) / len(filtered_data)    # filtered_data에서 bmi 평균 계산
    avg_bp_systolic = sum(data['bp_systolic'] for data in filtered_data) / len(filtered_data)   # filtered_data에서 수축기혈압 평균 계산
    avg_bp_diastolic = sum(data['bp_diastolic'] for data in filtered_data) / len(filtered_data)    # filtered_data에서 이완기혈압 평균 계산
    avg_glucose = sum(data['glucose'] for data in filtered_data) / len(filtered_data)   # filtered_data에서 공복혈당 평균 계산

    name = user_data['name']

    result = ''
    result += compare_value(name, 'BMI', bmi, avg_bmi) + '\n'
    result += compare_value(name, '수축기혈압', user_data['bp_systolic'], avg_bp_systolic) + '\n'
    result += compare_value(name, '이완기혈압', user_data['bp_diastolic'], avg_bp_diastolic) + '\n'
    result += compare_value(name, '공복혈당', user_data['glucose'], avg_glucose)

    return result


# '나의 건강 확인하기' 메뉴를 눌렀을 때 실행될 함수
def health_check():
    name, height, weight, bp_systolic, bp_diastolic, glucose = health_input()      # 사용자에게 키, 몸무게, 혈압, 혈당 입력받기
    
    bmi = calculate_bmi(height, weight)   # BMI 계산
    
    result_bmi = classify_bmi(bmi)                           # BMI 판별
    result_bp = classify_bp(bp_systolic, bp_diastolic)     # 혈압 판별
    result_glucose = classify_glucose(glucose)                       # 혈당 판별
    
    print(f'== {name}님의 건강 상태 ==')
    print(f'BMI : {bmi}')
    print(f'BMI 판정 : {result_bmi}')
    print(f'혈압 판정 : {result_bp}')
    print(f'혈당 판정 : {result_glucose}')
    

# '평균과 비교하기' 메뉴를 눌렀을 때 실행될 함수
def compare():
    name, height, weight, bp_systolic, bp_diastolic, glucose = health_input()
    gender, age_group = gender_age_input()

    user_data = {'name':name, 'gender':gender, 'age_group':age_group,
                'height':height, 'weight':weight,
                'bp_systolic':bp_systolic, 'bp_diastolic':bp_diastolic,
                'glucose':glucose}

    bmi = calculate_bmi(height, weight)       

    result_bmi = classify_bmi(bmi)
    result_bp = classify_bp(bp_systolic, bp_diastolic)
    result_glucose = classify_glucose(glucose)
    
    # 같은 성별·연령대 데이터 필터링
    filtered_data = [data for data in health_data
                        if data['gender'] == user_data['gender']
                        and data['age_group'] == user_data['age_group']]
    
    # 집단의 평균과 비교
    result_compare = compare_average(user_data, bmi, filtered_data)

    # 결과 출력
    print(f'== {name}님과 동일한 성별, 연령대 집단의 평균 건강상태 비교하기 ==')
    print(result_compare)


# 첫 화면 메뉴 함수
def main():
    while True:
        print('=== 건강 상태 판별 프로그램 ===')
        print('1. 나의 건강 확인하기')
        print('2. 평균과 비교하기')
        print('3. 종료')

        menu = input('메뉴 선택 : ')

        if menu == '1':
            health_check()
        elif menu == '2':
            compare()
        elif menu == '3':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 입력입니다.')




# 건강검진 데이터 불러오기 (AI 도움)
import zipfile
import csv

zip_path = r"C:/Users/Samsung/Desktop/컴퓨팅사고와 sw코딩/컴사_프로젝트/국민건강보험공단_건강검진정보_20241231.zip"

health_data = []

with zipfile.ZipFile(zip_path, 'r') as zip_file:
    csv_name = [name for name in zip_file.namelist() if name.lower().endswith('.csv')][0]

    with zip_file.open(csv_name) as csv_file:
        reader = csv.DictReader(
            (line.decode('cp949') for line in csv_file)
        )

        for row in reader:
            # 필요한 값 중 하나라도 비어 있으면 그 행은 건너뜀 (이 조건문 없으면 오류 발생 - AI 도움으로 해결)
            if (
                row['성별코드'] == '' or
                row['연령대코드(5세단위)'] == '' or
                row['신장(5cm단위)'] == '' or
                row['체중(5kg단위)'] == '' or
                row['수축기혈압'] == '' or
                row['이완기혈압'] == '' or
                row['식전혈당(공복혈당)'] == ''
            ):
                continue

            data = {
                'gender': int(row['성별코드']),
                'age_group': int(row['연령대코드(5세단위)']),
                'height': int(row['신장(5cm단위)']),
                'weight': int(row['체중(5kg단위)']),
                'bp_systolic': int(row['수축기혈압']),
                'bp_diastolic': int(row['이완기혈압']),
                'glucose': int(row['식전혈당(공복혈당)'])
            }

            health_data.append(data)

print(len(health_data))
print(health_data[0])



# GUI 구현
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("건강 수치 비교 프로그램")
root.geometry("500x700")


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def show_home():
    clear_window()

    title_label = tk.Label(root, text="건강 수치 비교 프로그램", font=("맑은 고딕", 18, "bold"))
    title_label.pack(pady=40)

    btn_health = tk.Button(root, text="건강 판별", width=20, height=2, command=show_health_check)
    btn_health.pack(pady=10)

    btn_compare = tk.Button(root, text="평균 비교", width=20, height=2, command=show_compare)
    btn_compare.pack(pady=10)

    btn_exit = tk.Button(root, text="종료", width=20, height=2, command=root.destroy)
    btn_exit.pack(pady=10)


def make_input(label_text):
    label = tk.Label(root, text=label_text)
    label.pack()

    entry = tk.Entry(root)
    entry.pack(pady=5)

    return entry


# 건강 판별 화면
def show_health_check():
    clear_window()

    title_label = tk.Label(root, text="건강 판별", font=("맑은 고딕", 16, "bold"))
    title_label.pack(pady=20)

    name_entry = make_input("이름")
    height_entry = make_input("키(cm)")
    weight_entry = make_input("몸무게(kg)")
    bp_systolic_entry = make_input("수축기혈압")
    bp_diastolic_entry = make_input("이완기혈압")
    glucose_entry = make_input("공복혈당")

    def check_result():
        try:
            name = name_entry.get()
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            bp_systolic = int(bp_systolic_entry.get())
            bp_diastolic = int(bp_diastolic_entry.get())
            glucose = int(glucose_entry.get())

            if name == "":
                messagebox.showerror("입력 오류", "이름을 입력하세요.")
                return

            if height <= 0 or weight <= 0 or bp_systolic <= 0 or bp_diastolic <= 0 or glucose <= 0:
                messagebox.showerror("입력 오류", "건강 수치는 0보다 큰 숫자로 입력하세요.")
                return

            bmi = calculate_bmi(height, weight)

            result_bmi = classify_bmi(bmi)
            result_bp = classify_bp(bp_systolic, bp_diastolic)
            result_glucose = classify_glucose(glucose)

            result_text = (
                f"== {name}님의 건강 상태 ==\n\n"
                f"BMI : {bmi}\n"
                f"BMI 판정 : {result_bmi}\n"
                f"혈압 판정 : {result_bp}\n"
                f"혈당 판정 : {result_glucose}"
            )

            messagebox.showinfo("건강 판별 결과", result_text)

        except ValueError:
            messagebox.showerror("입력 오류", "키, 몸무게, 혈압, 공복혈당은 숫자로 입력하세요.")

    btn_result = tk.Button(root, text="결과 확인", width=15, command=check_result)
    btn_result.pack(pady=15)

    btn_home = tk.Button(root, text="홈으로", width=15, command=show_home)
    btn_home.pack(pady=5)



# 평균 비교 화면
def show_compare():
    clear_window()

    title_label = tk.Label(root, text="평균 비교", font=("맑은 고딕", 16, "bold"))
    title_label.pack(pady=15)

    name_entry = make_input("이름")
    gender_entry = make_input("성별 (남자=1 / 여자=2)")
    age_entry = make_input("나이")
    height_entry = make_input("키(cm)")
    weight_entry = make_input("몸무게(kg)")
    bp_systolic_entry = make_input("수축기혈압")
    bp_diastolic_entry = make_input("이완기혈압")
    glucose_entry = make_input("공복혈당")

    def compare_result():
        try:
            name = name_entry.get()
            gender = int(gender_entry.get())
            age = int(age_entry.get())
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            bp_systolic = int(bp_systolic_entry.get())
            bp_diastolic = int(bp_diastolic_entry.get())
            glucose = int(glucose_entry.get())

            if name == "":
                messagebox.showerror("입력 오류", "이름을 입력하세요.")
                return

            if gender != 1 and gender != 2:
                messagebox.showerror("입력 오류", "성별은 1 또는 2만 입력하세요.")
                return

            if age < 0:
                messagebox.showerror("입력 오류", "나이는 0 이상으로 입력하세요.")
                return

            if height <= 0 or weight <= 0 or bp_systolic <= 0 or bp_diastolic <= 0 or glucose <= 0:
                messagebox.showerror("입력 오류", "건강 수치는 0보다 큰 숫자로 입력하세요.")
                return

            if age >= 85:
                age_group = 18
            else:
                age_group = (age // 5) + 1

            user_data = {
                "name": name,
                "gender": gender,
                "age_group": age_group,
                "height": height,
                "weight": weight,
                "bp_systolic": bp_systolic,
                "bp_diastolic": bp_diastolic,
                "glucose": glucose
            }

            bmi = calculate_bmi(height, weight)

            filtered_data = [
                data for data in health_data
                if data["gender"] == user_data["gender"]
                and data["age_group"] == user_data["age_group"]
            ]

            result_compare = compare_average(user_data, bmi, filtered_data)

            result_text = (
                f"== {name}님의 평균 비교 결과 ==\n\n"
                f"동일한 성별·연령대 데이터 수 : {len(filtered_data)}명\n"
                f"사용자 BMI : {bmi}\n\n"
                f"{result_compare}"
            )

            messagebox.showinfo("평균 비교 결과", result_text)

        except ValueError:
            messagebox.showerror("입력 오류", "성별, 나이, 건강 수치는 숫자로 입력하세요.")

    btn_result = tk.Button(root, text="비교 결과 확인", width=15, command=compare_result)
    btn_result.pack(pady=15)

    btn_home = tk.Button(root, text="홈으로", width=15, command=show_home)
    btn_home.pack(pady=5)


def make_input(label_text):
    label = tk.Label(root, text=label_text)
    label.pack()

    entry = tk.Entry(root)
    entry.pack(pady=5)

    return entry

show_home()
root.mainloop()



'''
GUI로 구현하기 전에 CLI로 코드 작성
GUI로 구현하면서 함수 일부 변경
GUI로 바꾸면서 필요없는 함수 제거됐는지 확인 필요
GUI에서 두번째 버튼 기능은 완성 덜함 (그래프, 평균, 표준편차 등 추가해야됨)
극단적인 값 넣었을때 대비 안해둠
함수 이름 헷갈려서 변경해야됨

'''