from pynput import keyboard
import pyaudio
import wave

keyboard_ctrl = keyboard.Controller()

def record(filename):
    def on_key_press(key):
        nonlocal recording
        if key == keyboard.Key.space:
            if not recording:
                recording = True
                print("Start recording audio...")       

    def on_key_release(key):
        nonlocal recording
        if key == keyboard.KeyCode.from_char('s') and recording:
            recording = False
            print("Stop recording")
            return False  # 停止监听键盘事件

    recording = False

    # 创建键盘监听器
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        p = pyaudio.PyAudio()
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024

        stream = p.open(rate=RATE,
                        format=FORMAT,
                        channels=CHANNELS,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        print("Press the 【spacebar】 to start recording audio, and press the 【's'】 key to stop recording.")

        while True:
            if recording:
                data = stream.read(CHUNK)
                frames.append(data)

            if not listener.is_alive():
                break

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')

        wf.setframerate(RATE)
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))

        wf.writeframes(b''.join(frames))
        wf.close()

if __name__ == "__main__":
    record("user_voice.wav")