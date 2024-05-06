from soft_pwm import PWM
import time

class Engines:
    
    def __init__(self, left_a, left_b, right_a, right_b):
        self.left_a = left_a
        self.left_b = left_b
        self.right_a = right_a
        self.right_b = right_b
        
        self.pwm = PWM(left_a, left_b, right_a, right_b)
        self.pwm.run_in_thread()
        
    def straight(self, power):
        self.pwm.set_pwm_duty_cycle(self.left_a, power)
        self.pwm.set_pwm_duty_cycle(self.right_a, power)
            
        self.pwm.set_pwm_duty_cycle(self.left_b, 0)
        self.pwm.set_pwm_duty_cycle(self.right_b, 0)
            
    def stop(self):
        self.pwm.set_pwm_duty_cycle(self.left_a, 0)
        self.pwm.set_pwm_duty_cycle(self.right_a, 0)
            
        self.pwm.set_pwm_duty_cycle(self.left_b, 0)
        self.pwm.set_pwm_duty_cycle(self.right_b, 0)
            

if __name__ == "__main__":
    engines = Engines(20, 21, 26, 19)
    engines.straight(10)
    time.sleep(2)
    engines.stop()
    time.sleep(2)
    engines.pwm.stop_thread()
    engines. pwm.cleanup_pins()