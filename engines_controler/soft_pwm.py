import RPi.GPIO as GPIO
import time
from threading import Thread
GPIO.setmode(GPIO.BCM)

class PWM:
    """create simple soft pwm with 10 duty cycle steps and periond 20 times per 1 second"""
    __PERIOD = 1/200 # 20 * 10 steps
    def __init__(self, *args):
        """ args - sequence numbers of pins wich will generate pwm"""
        self._used_pins = args
        self._pwms_duty_cycle = { i:0 for i in args}
        self.init_outputs()
        self._thread = Thread(target=self.run)
        self._thread_working = True
    
    def init_outputs(self):
        for pin in self._used_pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            
    def set_pwm_duty_cycle(self, pin, val):
        if val < 0 or val > 10:
            raise ValueError('value must be between 0-10')
        self._pwms_duty_cycle[pin] = val     
        
    def run(self):
        timer = 0
        while self._thread_working:
            time.sleep(self.__PERIOD)
            timer += 1
            if(timer == 200):   #restart timer every 1s
                timer = 0
            step_position = timer%10
            for pin in self._used_pins:
                    if(step_position == 0 and self._pwms_duty_cycle[pin] != 0):
                        GPIO.output(pin, GPIO.HIGH)
                    elif(step_position == self._pwms_duty_cycle[pin]):
                        GPIO.output(pin, GPIO.LOW)
                
    def run_in_thread(self):
        self._thread.start()
    
    def stop_thread(self):
        self._thread_working = False
        self._thread.join()
        
    def cleanup_pins(self):
        GPIO.cleanup()
        
if __name__ == "__main__":
    left_engine_pin_a = 20
    left_engine_pin_b = 21

    right_engine_pin_a = 26
    right_engine_pin_b = 19
    
    pwm = PWM(left_engine_pin_a, left_engine_pin_b, right_engine_pin_a, right_engine_pin_b)
    
    pwm.set_pwm_duty_cycle(left_engine_pin_a, 7)
    pwm.set_pwm_duty_cycle(left_engine_pin_b, 3)
    
    pwm.run_in_thread()
    time.sleep(4)
    pwm.stop_thread()
    pwm.cleanup_pins()