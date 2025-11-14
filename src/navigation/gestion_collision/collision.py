class collision:
    
    def __init__(self, radar):
        self.radar = radar
    
    def detecter_collision(self):
        
        distance = self.radar.obtenir_distance()
        if distance < 50:
            return True
        else:
            return False
