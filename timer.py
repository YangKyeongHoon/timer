import time
import os
import sys
import select
import tty
import termios

def countdown(t):
    """
    지정한 시간(초)만큼 카운트다운하는 함수.
    카운트다운 중 'q' 키를 누르면 종료됩니다.
    """
    # 터미널의 원본 설정을 저장합니다.
    original_settings = termios.tcgetattr(sys.stdin)
    
    try:
        # 터미널을 cbreak 모드로 설정하여 Enter 키 없이 바로 입력을 받습니다.
        tty.setcbreak(sys.stdin.fileno())
        
        while t > 0:
            mins, secs = divmod(t, 60)
            timer_format = '{:02d}:{:02d}'.format(mins, secs)
            print(timer_format, end='\r')
            
            # 1초 동안 sys.stdin (키보드 입력)을 감시합니다.
            rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
            
            if rlist:
                # 1초 안에 키 입력이 감지되면
                char = sys.stdin.read(1)
                if char.lower() == 'q':
                    print("\n타이머가 사용자에 의해 중지되었습니다.  ")
                    return # countdown 함수를 종료합니다.
            
            t -= 1

    finally:
        # 스크립트가 어떤 이유로든 종료될 때, 터미널 설정을 반드시 원래대로 복원합니다.
        # 이렇게 하지 않으면 터미널이 비정상적으로 동작할 수 있습니다.
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)

    print('타이머 종료!                  ') # 이전 텍스트를 덮어쓰기 위해 공백 추가
    for _ in range(10): # 10번 반복 재생
        os.system("afplay /System/Library/Sounds/Basso.aiff")

if __name__ == '__main__':
    try:
        # 사용자로부터 시간을 초 단위로 입력받습니다.
        seconds_input = input("타이머를 몇 초로 설정할까요? (종료: q) ")
        if seconds_input.lower() == 'q':
            sys.exit()
        seconds = int(seconds_input)
        countdown(seconds)
    except ValueError:
        print("오류: 유효한 숫자를 입력해주세요.")
    except KeyboardInterrupt:
        # 비상 탈출 경로로 남겨둡니다.
        print("\n타이머가 강제 중지되었습니다.")