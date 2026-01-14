import time

led_path = "/sys/class/leds/ACT/brightness"

while True:
    with open(led_path, "w") as f:
        f.write("1")  # ON
    time.sleep(1)
    with open(led_path, "w") as f:
        f.write("0")  # OFF
    time.sleep(1)
