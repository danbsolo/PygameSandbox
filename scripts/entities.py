
class PhysicsEntity:
    def __init__(self, game, entityType, position, size):
        self.game = game
        self.type = entityType
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        frameMovement = (movement[0]+self.velocity[0], movement[1]+self.velocity[1])

        self.position[0] += frameMovement[0]
        self.position[1] += frameMovement[1]
    
    def render(self, surface):
        surface.blit(self.game.assets["player"], self.position)