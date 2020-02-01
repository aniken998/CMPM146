# File containing Checks
import logging
# Are we out of Neutral Planets
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# Conserve resources
def save_fleet(state):
    return len(state.my_fleets()) > 5

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())