
import tkinter as tk
import os

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI 타이머")

        self.time_left = 0
        self.is_running = False
        self._job = None

        # 시간 표시 레이블
        self.time_label = tk.Label(root, text="00:00", font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        # 시간 입력 필드 프레임
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=10)

        tk.Label(self.entry_frame, text="분:").pack(side=tk.LEFT)
        self.min_entry = tk.Entry(self.entry_frame, width=5)
        self.min_entry.pack(side=tk.LEFT)
        self.min_entry.insert(0, "1") # 기본값으로 1분 설정

        tk.Label(self.entry_frame, text="초:").pack(side=tk.LEFT)
        self.sec_entry = tk.Entry(self.entry_frame, width=5)
        self.sec_entry.pack(side=tk.LEFT)
        self.sec_entry.insert(0, "30") # 기본값으로 30초 설정

        # 버튼 프레임
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="시작", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="정지", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="리셋", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.set_time() # 초기 시간 설정

    def set_time(self):
        if self.is_running:
            return
        try:
            mins = int(self.min_entry.get() or 0)
            secs = int(self.sec_entry.get() or 0)
            self.time_left = mins * 60 + secs
            self.update_label()
        except ValueError:
            self.time_label.config(text="숫자만!")

    def update_label(self):
        mins, secs = divmod(self.time_left, 60)
        timer_format = '{:02d}:{:02d}'.format(mins, secs)
        self.time_label.config(text=timer_format)

    def start_timer(self):
        if self.is_running:
            return
        self.set_time() # 시작 전에 시간 재설정
        if self.time_left == 0:
            return
        self.is_running = True
        self.countdown()

    def stop_timer(self):
        if self._job is not None:
            self.root.after_cancel(self._job)
            self._job = None
        self.is_running = False

    def reset_timer(self):
        self.stop_timer()
        self.set_time()

    def countdown(self):
        if self.is_running and self.time_left > 0:
            self.update_label()
            self.time_left -= 1
            self._job = self.root.after(1000, self.countdown)
        elif self.is_running and self.time_left == 0:
            self.update_label()
            self.is_running = False
            self.time_label.config(text="종료!")
            self._job = None
            # macOS에서 시스템 사운드 재생
            os.system("afplay /System/Library/Sounds/Basso.aiff")

if __name__ == '__main__':
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
