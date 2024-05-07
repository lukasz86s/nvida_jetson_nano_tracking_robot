from soft_pwm import PWM
import time

class Engines:
    
    def __init__(self, left_a, left_b, right_a, right_b):
        self.__left_a = left_a
        self.__left_b = left_b
        self.__right_a = right_a
        self.__right_b = right_b
        
        self.pwm = PWM(left_a, left_b, right_a, right_b)
        self.pwm.run_in_thread()
        
    def left_forward(self, power):
        self.pwm.set_pwm_duty_cycle(self.__left_a, power)
        self.pwm.set_pwm_duty_cycle(self.__left_b, 0)
        
    def left_backward(self, power):
        self.pwm.set_pwm_duty_cycle(self.__left_b, power)
        self.pwm.set_pwm_duty_cycle(self.__left_a, 0)
        
    def left_stop(self):
        self.pwm.set_pwm_duty_cycle(self.__left_b, 0)
        self.pwm.set_pwm_duty_cycle(self.__left_a, 0)
        
    def right_forward(self, power):
        self.pwm.set_pwm_duty_cycle(self.__right_a, power)
        self.pwm.set_pwm_duty_cycle(self.__right_b, 0)
        
    def right_basckward(self,power):
        self.pwm.set_pwm_duty_cycle(self.__right_b, power)
        self.pwm.set_pwm_duty_cycle(self.__right_a, 0)
        
    def right_stop(self):
        self.pwm.set_pwm_duty_cycle(self.__right_b, 0)
        self.pwm.set_pwm_duty_cycle(self.__right_a, 0)
        

class RobotMovement:
    def __init__(self, left_a, left_b, right_a, right_b):
        self._engines = Engines(left_a, left_b, right_a, right_b)
        
    def forward(self, power):
        self._engines.left_forward(power)
        self._engines.right_forward(power)
        
    def backward(self, power):
        self._engines.left_backward(power)
        self._engines.right_backward(power)    
        
    def stop(self):
        self._engines.left_stop()
        self._engines.right_stop()
        
    def kill_engines(self):
        if self._engines != None:
            self._engines.pwm.stop_thread()
            self._engines.pwm.cleanup_pins()
            del(self._engines)
            self._engines = None
        else:
            raise AttributeError("Caught an AttributeError! The object does not exist. First create new pwm instance")
    
    def create_engines(self, left_a, left_b, right_a, right_b):
        if self._engines == None:
            self._engines = Engines(left_a, left_b, right_a, right_b)
        else:
            raise AttributeError("AttributeError: Attempted to assign a value to a exist engines object")

if __name__ == "__main__":
    robot= RobotMovement(20, 21, 26, 19)
    robot.forward(3)
    time.sleep(2)
    robot.stop()
    time.sleep(2)
    robot.kill_engines()
    