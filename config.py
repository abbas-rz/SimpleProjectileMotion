InitialHeight = 0
Theta = 45 # angle in degrees
Velocity = 9
Gravity = -9.81  # m/s^2, negative because it acts downwards
# objectmass = 1 not used
import math


initialVelocityX = math.cos(math.radians(Theta)) * Velocity
initialVelocityY = math.sin(math.radians(Theta)) * Velocity

print(f"Initial Velocity X: {initialVelocityX:.2f} m/s")
print(f"Initial Velocity Y: {initialVelocityY:.2f} m/s")

