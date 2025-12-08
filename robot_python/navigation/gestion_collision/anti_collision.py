from navigation.gestion_collision.interfaces.i_collision import i_collision

class Anti_collision(i_collision):
    
    def __init__(self, radar):
        self.radar = radar
    
    def detecter_collision(self):
        
        distance = self.radar.obtenir_distance()
        if distance < 25:
            return True
        else:
            return False
