from datetime import datetime
import time

import sys
sys.path.append("/tflow")
from tflow import detect

class correct_path_follower():
    def __init__(self, pair, color,dist, previous_error, accum_error,time_difference1, time_difference2, target_light,fixed_speed,current_time, kp, kd, ki):

        self.pair=pair
        self.color=color
        self.dist=dist
        self.previous_error=previous_error
        self.accum_error=accum_error
        self.time_difference1=time_difference1
        self.time_difference2=time_difference2
        self.current_time=current_time
        self.target_light=target_light
        self.fixed_speed=fixed_speed
        self.kp=kp  
        self.ki=ki
        self.kd=kd
   
        
    
    ### The  path following function:::
    def path_follow(self):  
		#global previous_error, accum_error, time_difference1,time_difference2, current_time
		# Propotional(P)	
        current_error=self.color.get_reflected_light() - self.target_light
		# Differential (D)
        error_difference=current_error-self.previous_error
			# Integral (I)
        self.accum_error = self.accum_error + current_error
		#print(current_error , " ce " , error_difference , "ed" , accum_error , "ae" )
			
		#With PID correction : 
        new_speed=current_error*self.kp +(self.accum_error*self.ki*self.time_difference1)+(error_difference*self.kd/self.time_difference2)
        #print("new_speed",new_speed, "**", error_difference*self.kd)
		# adjust speed:::
        self.pair.start(-abs(self.fixed_speed-new_speed), abs(self.fixed_speed  + new_speed)) 
		
        # Reassign values for next round
        self.previous_error = current_error
        self.previous_time= self.current_time
        self.current_time = datetime.now()
        self.time_difference1= (self.current_time-self.previous_time).total_seconds()
        self.time_difference2= self.time_difference1
       
        return self.previous_error, self.previous_time, self.current_time,self.time_difference1, self.time_difference2
	    

    
	## Act based on current Distance:::
    def distance_cal(self):
        #self.phase2_obj.detect_obj()
        
        global previous_error, previous_time, current_time ,time_difference1, time_difference2
        #self.phase2_obj.pass_QR() 
        
        distance=self.dist.get_distance()
        ## If there is no obstacle:::
        if distance > 150 or distance ==-1:
            previous_error, previous_time, current_time ,time_difference1, time_difference2=self.path_follow()

        else:
            self.check_object()
            # Avoid the obstacle:::
            #previous_error, current_time ,time_difference1, time_difference2=self.obstacle_avoid()
         
    #### Turning different directions
    def turn_right(self):
        self.pair.run_for_degrees(225,-20,-20)
        self.pair.stop()
        time.sleep(.5)

    def turn_left(self):
        self.pair.run_for_degrees(225,20,20)
        self.pair.stop()
        time.sleep(.5)
        
    #### Moving  front  :

    def move_forward(self):
        self.pair.run_for_rotations(2,-60,60)
        self.pair.stop()
        time.sleep(.5)
      
    ### here we give code to go here and there based on the train data  
    def check_object(self):
        self.pair.stop()
        detect.detect_run()
        time.sleep(1)
        self.turn_left
        time.sleep(.5)
        ### We need to process data, but this should give output as left right::
        '''
        data=detect.detect_run()
        if data=='left':
            self.turn_left()
        elif data=='right': 
            self.turn_right()
        else:
            self.pair.stop()      
        '''
