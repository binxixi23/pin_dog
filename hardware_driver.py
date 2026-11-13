import time
from pidog import Pidog


class LowGravityDog:
    """
    Bo dieu khien PiDog toi uu trong tam thap (Low Center of Gravity)
    Giup robot di chuyen cham, dam chac va chong lat ngang.
    """

    def __init__(self):
        self.bot = Pidog()
        self.walk_speed = 70
        self.servo_speed = 80
        self.head_speed = 75

    def wait_s(self, sec):
        time.sleep(sec)

    def say(self, message):
        print(f"[pin_dog]: {message}")
        self.bot.speak(message)
        self.wait_s(0.4)

    def led_status(self, color_name, blink_rate=2):
        color_map = {
            "amber": "yellow",
            "emerald": "green",
            "crimson": "red",
            "ice_blue": "cyan",
            "purple": "pink",
        }
        safe_color = color_map.get(color_name, "white")
        self.bot.rgb_strip.set_mode("breath", safe_color, bps=blink_rate)

    def crouch_stance(self):
        """
        Ha thap toan than (khuyu chan) de ha trong tam truoc khi di chuyen.
        """
        low_posture = [
            [-25, 65, -25, 65, -25, 65, -25, 65]
        ]
        self.bot.legs_move(low_posture, immediately=True, speed=self.servo_speed)
        self.bot.wait_legs_done()
        self.bot.head_move([[0, 0, -5]], immediately=True, speed=self.head_speed)
        self.bot.wait_head_done()
        self.wait_s(0.6)

    def rest_posture(self):
        """Ha han bung xuong san nghi ngoi an toan."""
        self.bot.do_action("lie", speed=70)
        self.bot.wait_legs_done()
        self.wait_s(0.8)

    def center_calibration(self):
        """Can chinh tat ca khop ve vi tri thap an toan."""
        self.crouch_stance()
        for angle in [12, -12, 0]:
            self.bot.head_move([[angle, 0, -5]], immediately=True, speed=self.head_speed)
            self.bot.wait_head_done()
            self.wait_s(0.4)
        self.bot.do_action("wag_tail", step_count=3, speed=90)
        self.bot.wait_legs_done()

    def slow_step_forward(self, num_steps=2):
        """Di toi tung buoc cham tu tu the ha thap trong tam."""
        self.crouch_stance()
        for _ in range(num_steps):
            self.bot.do_action("forward", step_count=1, speed=self.walk_speed)
            self.bot.wait_legs_done()
            self.crouch_stance()
            self.wait_s(0.5)

    def slow_step_backward(self, num_steps=2):
        """Di lui tung buoc cham tu tu the ha thap trong tam."""
        self.crouch_stance()
        for _ in range(num_steps):
            self.bot.do_action("backward", step_count=1, speed=self.walk_speed)
            self.bot.wait_legs_done()
            self.crouch_stance()
            self.wait_s(0.5)

    def gentle_tail_and_nod(self):
        """Dong tac nhe nhang khi choi nhac (khong lac dau manh)."""
        self.bot.do_action("wag_tail", step_count=4, speed=85)
        self.bot.head_move([[0, 0, 5]], immediately=True, speed=65)
        self.bot.wait_head_done()
        self.wait_s(0.5)
        self.bot.head_move([[0, 0, -5]], immediately=True, speed=65)
        self.bot.wait_head_done()

    def shutdown(self):
        self.rest_posture()
        self.bot.close()
