# bmi 계산하는 함수
def calculate_bmi(height, weight):
    height_m = height/100    # cm로 입력받은 키를 m로 변환
    bmi = round(weight / (height_m**2), 2)    # bmi 계산
    return bmi    # 계산한 bmi 반환


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


# 그래프 그리는 데 필요한 라이브러리 (AI 도움)
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# 통계 정보(평균, 표준편차, 백분위수) 텍스트를 만드는 함수 (AI 도움)
def make_stat_text(name, item_name, data_list, user_value):
    n = len(data_list)
    mean = sum(data_list) / n  # 평균 계산
    variance = sum((x - mean) ** 2 for x in data_list) / n  # 분산 계산
    std = variance ** 0.5  # 표준편차 계산

    count_below = sum(1 for v in data_list if v < user_value)  # 사용자보다 작은 값의 개수
    percentile = round(count_below / n * 100, 1)  # 백분위수 계산

    text = (
        f'평균: {mean:.1f} / 표준편차: {std:.1f}\n'
        f'{name}님의 값: {user_value} (상위 {100 - percentile:.1f}%)'
    )
    return text


# 분포 그래프 + 사용자 위치 표시하는 함수 (영어 라벨로 표시)
def plot_distribution(parent, data_list, user_value, title, xlabel, xlim=None):
    fig, ax = plt.subplots(figsize=(4, 3))

    ax.hist(data_list, bins=20, color='skyblue', edgecolor='black')  # 전체 분포 히스토그램
    ax.axvline(user_value, color='red', linewidth=2, label=f'My value: {user_value}')  # 사용자 위치 표시 (빨간 세로선)

    if xlim is not None:
        ax.set_xlim(xlim)  # x축 범위 제한

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Number of people')
    ax.legend()

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)  # tkinter 창에 그래프 넣기
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5)


# 혈압 분포 그래프(수축기+이완기) 그리는 함수
def plot_bp_distribution(parent, sys_list, dia_list, user_sys, user_dia):
    fig, ax = plt.subplots(figsize=(4, 3))

    ax.hist(sys_list, bins=20, color='skyblue', alpha=0.6, label='Systolic (group)')  # 수축기혈압 분포
    ax.hist(dia_list, bins=20, color='lightgreen', alpha=0.6, label='Diastolic (group)')  # 이완기혈압 분포

    ax.axvline(user_sys, color='red', linewidth=2, label=f'My Systolic: {user_sys}')  # 사용자 수축기혈압 위치
    ax.axvline(user_dia, color='darkgreen', linewidth=2, linestyle='--', label=f'My Diastolic: {user_dia}')  # 사용자 이완기혈압 위치

    ax.set_title('Blood Pressure Distribution')
    ax.set_xlabel('Blood Pressure')
    ax.set_ylabel('Number of people')
    ax.legend(fontsize=8)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5)


# 비교 결과 화면에 3개 분포 그래프(BMI, 혈압, 혈당) + 통계 정보 텍스트를 보여주는 함수
def show_distribution_graphs(user_data, bmi, filtered_data):
    graph_window = tk.Toplevel(root)   # 새 창 띄우기
    graph_window.title("건강 수치 분포 그래프")
    graph_window.geometry("1300x600")

    name = user_data['name']

    # 같은 그룹의 BMI/혈압/혈당 리스트 계산
    bmi_list = [calculate_bmi(data['height'], data['weight']) for data in filtered_data]
    bp_systolic_list = [data['bp_systolic'] for data in filtered_data]
    bp_diastolic_list = [data['bp_diastolic'] for data in filtered_data]
    glucose_list = [data['glucose'] for data in filtered_data]

    # 그래프를 가로로 3개 배치하기 위한 프레임
    frame = tk.Frame(graph_window)
    frame.pack(fill='both', expand=True)

    frame_bmi = tk.Frame(frame)
    frame_bmi.pack(side='left', expand=True, fill='both')

    frame_bp = tk.Frame(frame)
    frame_bp.pack(side='left', expand=True, fill='both')

    frame_glucose = tk.Frame(frame)
    frame_glucose.pack(side='left', expand=True, fill='both')

    # 그래프 그리기 (혈당은 x축 범위를 0~250으로 제한)
    plot_distribution(frame_bmi, bmi_list, bmi, 'BMI Distribution', 'BMI')
    plot_bp_distribution(frame_bp, bp_systolic_list, bp_diastolic_list,
                          user_data['bp_systolic'], user_data['bp_diastolic'])
    plot_distribution(frame_glucose, glucose_list, user_data['glucose'], 'Glucose Distribution', 'Glucose', xlim=(0, 250))

    # 그래프 아래에 통계 정보(평균, 표준편차, 사용자 위치) 표시 (글씨 크기 키움)
    label_bmi = tk.Label(frame_bmi, text=make_stat_text(name, 'BMI', bmi_list, bmi),
                          font=("맑은 고딕", 12), justify='center')
    label_bmi.pack(pady=5)

    label_bp_sys = tk.Label(frame_bp, text=make_stat_text(name, '수축기혈압', bp_systolic_list, user_data['bp_systolic']),
                             font=("맑은 고딕", 12), justify='center')
    label_bp_sys.pack(pady=2)

    label_bp_dia = tk.Label(frame_bp, text=make_stat_text(name, '이완기혈압', bp_diastolic_list, user_data['bp_diastolic']),
                             font=("맑은 고딕", 12), justify='center')
    label_bp_dia.pack(pady=2)

    label_glucose = tk.Label(frame_glucose, text=make_stat_text(name, '공복혈당', glucose_list, user_data['glucose']),
                              font=("맑은 고딕", 12), justify='center')
    label_glucose.pack(pady=5)


# GUI 구현
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("건강 수치 비교 프로그램")
root.geometry("500x700")


# 화면을 초기화(기존 위젯 삭제)하는 함수
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


# 첫 화면(홈 화면)을 보여주는 함수
def show_home():
    clear_window()

    title_label = tk.Label(root, text="건강 수치 비교 프로그램", font=("맑은 고딕", 18, "bold"))
    title_label.pack(pady=40)

    btn_health = tk.Button(root, text="건강 판별", width=20, height=2, command=show_health_check)
    btn_health.pack(pady=10)

    btn_compare = tk.Button(root, text="건강 분포 확인하기", width=20, height=2, command=show_compare)
    btn_compare.pack(pady=10)

    btn_exit = tk.Button(root, text="종료", width=20, height=2, command=root.destroy)
    btn_exit.pack(pady=10)


# 라벨 + 입력칸을 만들어서 화면에 배치하는 함수
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

    # 입력값으로 BMI/혈압/혈당을 판정하고 결과를 보여주는 함수
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

            if height > 250 or weight > 300 or bp_systolic > 300 or bp_diastolic > 200 or glucose > 600:
                messagebox.showerror("입력 오류", "현실적인 범위의 값을 입력하세요.")
                return

            bmi = calculate_bmi(height, weight)

            result_bmi = classify_bmi(bmi)
            result_bp = classify_bp(bp_systolic, bp_diastolic)
            result_glucose = classify_glucose(glucose)

            # 문장 사이 간격을 위해 줄바꿈 두 번씩 사용
            result_text = (
                f"== {name}님의 건강 상태 ==\n\n\n"
                f"BMI : {bmi}\n\n"
                f"BMI 판정 : {result_bmi}\n\n"
                f"혈압 판정 : {result_bp}\n\n"
                f"혈당 판정 : {result_glucose}"
            )

            # 결과창 크기 키우기
            result_window = tk.Toplevel(root)
            result_window.title("건강 판별 결과")
            result_window.geometry("400x350")

            label = tk.Label(result_window, text=result_text, font=("맑은 고딕", 12), justify='left', padx=20, pady=20)
            label.pack()

            btn_close = tk.Button(result_window, text="닫기", command=result_window.destroy)
            btn_close.pack(pady=10)

        except ValueError:
            messagebox.showerror("입력 오류", "키, 몸무게, 혈압, 공복혈당은 숫자로 입력하세요.")

    btn_result = tk.Button(root, text="결과 확인", width=15, command=check_result)
    btn_result.pack(pady=15)

    btn_home = tk.Button(root, text="홈으로", width=15, command=show_home)
    btn_home.pack(pady=5)


# 건강 분포 확인하기 화면
def show_compare():
    clear_window()

    title_label = tk.Label(root, text="건강 분포 확인하기", font=("맑은 고딕", 16, "bold"))
    title_label.pack(pady=15)

    name_entry = make_input("이름")
    gender_entry = make_input("성별 (남자=1 / 여자=2)")
    age_entry = make_input("나이")
    height_entry = make_input("키(cm)")
    weight_entry = make_input("몸무게(kg)")
    bp_systolic_entry = make_input("수축기혈압")
    bp_diastolic_entry = make_input("이완기혈압")
    glucose_entry = make_input("공복혈당")

    # 입력값으로 BMI를 계산하고, 같은 성별/연령대 그룹과 비교하는 분포 그래프를 보여주는 함수
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

            # 극단적인 값 넣었을때 경고하도록 수정
            if age < 0 or age > 120:
                messagebox.showerror("입력 오류", "나이는 0~120 사이로 입력하세요.")
                return

            if height <= 0 or weight <= 0 or bp_systolic <= 0 or bp_diastolic <= 0 or glucose <= 0:
                messagebox.showerror("입력 오류", "건강 수치는 0보다 큰 숫자로 입력하세요.")
                return

            # 극단적인 값 넣었을때 경고하도록 수정
            if height > 250 or weight > 300 or bp_systolic > 300 or bp_diastolic > 200 or glucose > 600:
                messagebox.showerror("입력 오류", "현실적인 범위의 값을 입력하세요.")
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

            # 같은 성별·연령대 데이터 필터링
            filtered_data = [
                data for data in health_data
                if data["gender"] == user_data["gender"]
                and data["age_group"] == user_data["age_group"]
            ]

            # 분포 그래프 창 띄우기
            show_distribution_graphs(user_data, bmi, filtered_data)

        except ValueError:
            messagebox.showerror("입력 오류", "성별, 나이, 건강 수치는 숫자로 입력하세요.")

    btn_result = tk.Button(root, text="결과 확인", width=15, command=compare_result)
    btn_result.pack(pady=15)

    btn_home = tk.Button(root, text="홈으로", width=15, command=show_home)
    btn_home.pack(pady=5)


show_home()
root.mainloop()