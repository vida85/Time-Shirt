import bge

class Watch:
    def __init__(self) -> None:
        self.scene = bge.logic.getCurrentScene() 
        self.hand_watch = self.scene.objects['hand_watch']

    def put_watch_on(self, ON: bool):
        self.hand_watch.setVisible(ON)


class Timer:
    def __init__(self, hour, minute) -> None:
        self.hour = hour
        self.minute = minute
        self.scene = bge.logic.getCurrentScene() 

        self.time = self.scene.objects['watch_time']
        self.time['Text'] = " "

        self.watch_time = ""
        self.one = 59
        self.second = 0
        self.count = 0


    def timing(self) -> str:
        self.count += 1
        day_night = 'PM' if self.hour <= 12 else 'AM'
        if self.count > self.one:
            self.second += 1
            self.count = 0

            if self.second > self.one:
                self.minute += 1
                self.second = 0
        
                if self.minute > self.one:
                    self.minute = 0
                    self.hour += 1

        seconds = self.second if self.second > 9 else '0' + str(self.second)
        minutes = self.minute if self.minute > 9 else '0' + str(self.minute)
        self.watch_time = f"{self.hour}:{minutes}:{seconds} {day_night}"
        
        return self.watch_time
    
    
    def get_time(self) -> str:
        return self.watch_time
    

timer = Timer(hour=7, minute=59)