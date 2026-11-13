"""
pin_dog - Low-Center-of-Gravity PiDog Control System
Author: Cuong Dang
"""

import os
import subprocess
from hardware_driver import LowGravityDog

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
HOLIDAY_TRACK = os.path.join(BASE_FOLDER, "music", "christmas.wav")


def play_holiday_audio(dog):
    """
    Phat file nhac WAV neu co trong thu muc music/.
    Neu chua copy file nhac, tu dong phat giai dieu Jingle Bells bang am thanh he thong.
    """
    if os.path.exists(HOLIDAY_TRACK):
        print(f"Playing audio file: {HOLIDAY_TRACK}")
        return subprocess.Popen(["aplay", HOLIDAY_TRACK])
    else:
        print("No WAV file found. Playing built-in holiday melody...")
        # Giai dieu Jingle Bells don gian qua speaker
        jingle_notes = [
            "E5", "E5", "E5", "pause",
            "E5", "E5", "E5", "pause",
            "E5", "G5", "C5", "D5", "E5"
        ]
        for note in jingle_notes:
            if note == "pause":
                dog.wait_s(0.25)
            else:
                try:
                    dog.bot.music.sound_play_threading(note)
                except Exception:
                    pass
                dog.wait_s(0.3)
        return None


def run_step_one(dog):
    print("\n--- [1] CALIBRATION & LOW-STANCE WARMUP ---")
    dog.led_status("amber", blink_rate=2)
    dog.say("Starting calibration. Lowering center of gravity.")
    dog.center_calibration()
    dog.led_status("emerald", blink_rate=2)
    dog.say("Calibration finished. Balance is stable.")


def run_step_two(dog):
    print("\n--- [2] SAFE LOW-STANCE LOCOMOTION ---")
    dog.led_status("ice_blue", blink_rate=2)
    dog.say("Moving forward slowly.")
    dog.slow_step_forward(num_steps=2)

    dog.wait_s(0.8)
    dog.say("Moving backward slowly.")
    dog.slow_step_backward(num_steps=2)

    dog.led_status("emerald", blink_rate=2)
    dog.say("Locomotion test complete.")


def run_step_three(dog):
    print("\n--- [3] CHRISTMAS MELODY & CLOSING ---")
    # Ha nam sat san truoc khi choi nhac de dam bao khong bao gio nga
    dog.rest_posture()
    dog.led_status("crimson", blink_rate=2)
    dog.say("Merry Christmas! Here is a holiday song for you.")

    audio_proc = play_holiday_audio(dog)

    try:
        dog.led_status("crimson", blink_rate=3)
        dog.gentle_tail_and_nod()
        dog.wait_s(1.5)

        dog.led_status("emerald", blink_rate=3)
        dog.gentle_tail_and_nod()
        dog.wait_s(1.5)
    finally:
        if audio_proc is not None:
            audio_proc.terminate()

    # Loi cam on cuoi cung
    dog.led_status("emerald", blink_rate=2)
    dog.say("Thank you for taking the time to watch my demonstration. Goodbye!")


def start_console():
    dog = LowGravityDog()
    try:
        while True:
            print("\n==========================================")
            print("         PIN_DOG CONTROL CONSOLE          ")
            print("==========================================")
            print("1. Calibration & Low-Stance Warm-up")
            print("2. Safe Movements (Low-Stance Forward/Back)")
            print("3. Christmas Music & Thank You")
            print("4. Exit")

            selection = input("\nChoose an option (1-4): ").strip()

            if selection == "1":
                run_step_one(dog)
            elif selection == "2":
                run_step_two(dog)
            elif selection == "3":
                run_step_three(dog)
            elif selection == "4":
                dog.say("Thank you for watching. Powering down.")
                break
            else:
                print("Invalid input. Please choose 1, 2, 3, or 4.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        dog.shutdown()


if __name__ == "__main__":
    start_console()
