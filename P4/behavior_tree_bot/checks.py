# File containing Checks

# Are we out of Neutral Planets
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# Secondary call to get source to dest
def if_neutral_planet_near(state):
    # Check distance from closest planet to neutral target
    pass

# Am I being targeted?
def if_enemy_planet_attack(state):
    # (1) If Enemy currently has a fleet in flight
    if len(state.enemy_fleets()) >= 1:
        # (2) Check distance of their fleet to target
        for (fleet in state.enemy_fleets):
            target = fleet.destination_planet
            # print("Targetting,", target)
            if target in state.my_planets():
                return True
    return False


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())