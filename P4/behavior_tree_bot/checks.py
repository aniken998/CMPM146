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

# Conserve resources
def save_fleet(state):
    return len(state.my_fleets()) > 5

#return if enemy is attacking
def if_planet_got_attack(state):
    return len(state.enemy_fleets()) > 0

#return if the my strongest planet has less than 50 ships (all planets has less than 50 ships)
def has_enough_ships(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    if(ships == None):
        return False
    return strongest_planet.num_ships < 50

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_larger_growth(state):
    return (sum(planet.growth_rate for planet in state.my_planets())
           > sum(planet.growth_rate for planet in state.enemy_planets()) )

def have_more_conquest(state):
    return len(state.my_planets()) > len(state.enemy_planets())

def have_less_conquest(state):
    return len(state.my_planets()) <= len(state.enemy_planets())

def steal_fleet(state):
    total = sum(planet.num_ships for planet in state.my_planets())
    for fleet in state.enemy_fleets(): 
        target = fleet.destination_planet
        # Can steal a planet
        if fleet.num_ships < total:
            return True
    return False

#return if enemy is attacking
# def if_planet_got_attack(state):
#     return len(state.enemy_fleets()) > 0

# #return if the my strongest planet has less than 50 ships (all planets has less than 50 ships)
# def check_ship_left(state):
#     planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
#     if planet != None:
#         return planet.num_ships < 50
#     return False



