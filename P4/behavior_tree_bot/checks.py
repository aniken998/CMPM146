# File containing Checks
import logging
# Are we out of Neutral Planets
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# Spread to increase resources
def need_econ(state):
    # (1) Check econ of our planets
    for planet in state.my_planets():
        if planet.growth_rate < 10:
            return True
    return False

# Conserve resources, when we send more than we produce
def save_fleet(state):
    return len(state.my_fleets()) > 5
    #return (sum(fleet.num_ships for fleet in state.my_fleets()) \
    #    > sum(planet.growth_rate for planet in state.my_planets()))


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_larger_growth(state):
    return (sum(planet.growth_rate for planet in state.my_planets())
           > sum(planet.growth_rate for planet in state.enemy_planets()) )

def have_more_conquest(state):
    return (sum(planet for planet in state.my_planets())
           > sum(planet for planet in state.enemy_planets()) )