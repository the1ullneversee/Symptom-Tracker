
class activity():

    def __init__(self,name,type,completed):
        self.name = name
        self.type = type
        self.completed = completed
    
    def get_name(self):
        return self.name

    def get_completed(self):
        return self.completed
    
    def get_type(self):
        return self.type