import led
import time

def main():
    print("mp led test")
    led.init()

    while True:
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)

if __name__ == "__main__":
    main()