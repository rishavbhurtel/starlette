class Info:
    def __init__(self,info):
        self.id = info['id']
        self.name = info['name']
        self.address = info['address']
    
    def to_dict(self):
        return vars(self)