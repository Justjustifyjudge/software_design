import threading
import winsound

"""
Author: 林一凡
Time: 2024年6月5日15:55:09
蜂鸣器发声函数，用于烟雾检测报警
"""
def beep_sound(frequency, duration):
    winsound.Beep(frequency, duration)

"""
Author: 林一凡
Time: 2024年6月5日15:56:53
.wav播放方法，用于识别到陌生人脸时提醒
"""
def play_sound(file_path):
    winsound.PlaySound(file_path, winsound.SND_ASYNC | winsound.SND_FILENAME)

"""
Author: 林一凡
Time: 2024年6月5日15:58:57
烟雾火焰置信度超过阈值时创建线程并播放蜂鸣
"""
def alarm_smoke():
    beep_thread = threading.Thread(target=beep_sound, args=(1000, 500))
    beep_thread.start()

def recognize_person():
    sound_thread = threading.Thread(target=play_sound, args=('music.wav',))
    sound_thread.start()