import pygame

class PhysicsEntity:
    def __init__(self, game, entityType, position, size):
        self.game = game
        self.type = entityType
        self.position = list(position)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.isGrounded = False

    def getCollisionBox(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frameMovement = (movement[0]+self.velocity[0], movement[1]+self.velocity[1])
        
        self.position[0] += frameMovement[0]
        entityBox = self.getCollisionBox()
        for collisionBox in tilemap.getSurroundingCollisionBoxes(self.position):
            if entityBox.colliderect(collisionBox):
                if frameMovement[0] > 0:  # moving right
                    entityBox.right = collisionBox.left
                    self.collisions['right'] = True
                elif frameMovement[0] < 0:  # moving left
                    entityBox.left = collisionBox.right
                    self.collisions['left'] = True 
                self.position[0] = entityBox.x

        self.position[1] += frameMovement[1]
        entityBox = self.getCollisionBox()
        for collisionBox in tilemap.getSurroundingCollisionBoxes(self.position):
            if entityBox.colliderect(collisionBox):
                if frameMovement[1] > 0:  # moving down
                    entityBox.bottom = collisionBox.top
                    self.collisions['down'] = True
                elif frameMovement[1] < 0:  # moving up
                    entityBox.top = collisionBox.bottom
                    self.collisions['up'] = True
                self.position[1] = entityBox.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)  # ensures a terminal velocity (i.e. a cap) exists

        if self.collisions['down']:
            self.velocity[1] = 1  # ensures downward collision is always True if on the ground
            self.isGrounded = True
        else:
            self.isGrounded = False

        if self.collisions['up']:
            self.velocity[1] = 1

    
    def render(self, surface):
        surface.blit(self.game.assets["player"], self.position)
