# File containing Checks
import logging
# Are we out of Neutral Planets
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# Am I being targeted?
def if_enemy_planet_attack(state):
    for fleet in state.enemy_fleets():
        target = fleet.destination_planet
        logging.debug(str(target))
        logging.debug("Size of Fleet")
        logging.debug(str(fleet.num_ships))
        if target in state.my_planets():
            return any(state.my_planets())
    return False

# Check to see if a fleet is already traveling to a location.
def is_busy_reinforce(state):
    visited = []
    for fleet in state.my_fleets():
        target = fleet.destination_planet
        visited.append(target)
    for fleet in state.enemy_fleets():
        target = fleet.destination_planet
        if target in visited:
            return True
    return False

# Conserve resources
def save_fleet(state):
    return len(state.my_fleets()) > 5

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())