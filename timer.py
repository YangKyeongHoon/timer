import time
import os

def countdown(t):
    """
    지정한 시간(초)만큼 카운트다운하는 함수
    """
    while t:
        # divmod 함수를 사용해 분과 초를 계산합니다.
        mins, secs = divmod(t, 60)
        # 시간 형식을 00:00으로 맞춥니다.
        timer_format = '{:02d}:{:02d}'.format(mins, secs)
        # 같은 줄에 시간을 덮어쓰기 위해 end=''를 사용합니다.
        print(timer_format, end='\r')
        time.sleep(1)
        t -= 1

    print('타이머 종료!')
    for _ in range(10): # 10번 반복 재생
        os.system("afplay /System/Library/Sounds/Basso.aiff")

if __name__ == '__main__':
    try:
        # 사용자로부터 시간을 초 단위로 입력받습니다.
        seconds = int(input("타이머를 몇 초로 설정할까요? "))
        countdown(seconds)
    except ValueError:
        print("오류: 유효한 숫자를 입력해주세요.")
