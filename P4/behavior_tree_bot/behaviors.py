import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

# Want to insert a special case to supply planets when their growth exceeds an amount.


# Complex Attack
def attack_weakest_enemy_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    send = 0
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                send += 1
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            elif my_planet.num_ships > required_ships/2:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships/2)
                send += 1
                my_planet = next(my_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        if send > 0:
            return True
        else:
            return False


# Complex Spread
def spread_to_weakest_neutral_planet(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    neutral_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    neutral_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(neutral_planets)

    send = 0
    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                send += 1
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)

    except StopIteration:
        if send > 0:
            return True
        else:
            return False

# Complex Growth, Make it factor in distance and growth rate.
# Simple Growth
def spread_ally(state):
    # (1) Get the highest growth rate planet currently owned.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    # Make sure the strongest planet is willing to lose some ships.
    if (strongest_planet.growth_rate < 10):
        return False

    # (2) Search for some new planets to grow.
    for target_planet in state.my_planets():
        # New planet with less than 50 pop.
        if target_planet.growth_rate < 5:
            weakest_planet = target_planet

    # (3) Validify the action
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Increase the eco of the ally planet
    # Try to get atleast 100 ships there
    # Improvement: Try to save at least the mean of the enemy ships.
    strongest_threat = max(state.enemy_fleet(), key=lambda t: t.num_ships, default=None)

    # (5) Leave just enough to defend, allow risk in econ to decimate enemy numbers.
    estimated_risk = strongest_threat.num_ships
    if (estimated_risk < strongest_planet.num_ships):
        reinforcements = abs(estimated_risk - (weakest_planet - strongest_planet))
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, reinforcements)
    else:
        return False

# Does nothing. Just gain free econ and sit back.
def do_no_op(state):
    return True
    
# def protect_planet(state):
#     if len(state.my_fleets()) >= 3: # Max 3 on offense.
#         return False

#     strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

#     weakest_planet = max(state.my_planets(), key=lambda t: t.growth_rate, default=None)

#     shipsInFleet = 0
#     for fleet in state.my_fleets():
#         if(fleet.destination_planet == weakest_planet):
#             shipsInFleet = fleet.num_ships
#             break
    
#     if strongest_planet == None or weakest_planet == None:
#         return False

#     if weakest_planet.num_ships + shipsInFleet > 60:
#         return False

#     return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships/2)

def defendPlanet(state):
    my_planets = [planet for planet in state.my_planets()]

    if not my_planets:
        return False

    def strength(p):
        return p.num_ships \
               + sum(fleet.num_ships for fleet in state.my_fleets() if fleet.destination_planet == p.ID) \
               - sum(fleet.num_ships for fleet in state.enemy_fleets() if fleet.destination_planet == p.ID)

    avg = sum(strength(planet) for planet in my_planets) / len(my_planets)
    
    weak_planets = [planet for planet in my_planets if strength(planet) < avg]
    strong_planets = [planet for planet in my_planets if strength(planet) > avg]

    if (not weak_planets) or (not strong_planets):
        return False

    weak_planets = iter(sorted(weak_planets, key=strength))
    strong_planets = iter(sorted(strong_planets, key=strength, reverse=True))

    try:
        weak_planet = next(weak_planets)
        strong_planet = next(strong_planets)
        while True:
            need = int(avg - strength(weak_planet))
            have = int(strength(strong_planet) - avg)

            if have >= need > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, need)
                weak_planet = next(weak_planets)
            elif have > 0:
                issue_order(state, strong_planet.ID, weak_planet.ID, have)
                strong_planet = next(strong_planets)
            else:
                strong_planet = next(strong_planets)

    except StopIteration:
        return True

    return True

def steal_planet(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    steal_planets = min(state.not_my_planets(), key=lambda t: t.num_ships, default=None)
    if(steal_planets == None):
        return False

    steal_planet_ID = steal_planets.ID
    if(strongest_planet.num_ships < 50):
        return False
    
    for fleet in state.enemy_fleets(): 
        target = fleet.destination_planet
        # Can steal a planet
        if strongest_planet.num_ships > fleet.num_ships:
            steal_planet_ID = target

        # Chosen a planet to steal, check if it exists
        if (strongest_planet == None) or (steal_planet == None):            
            return False
    return issue_order(state, strongest_planet.ID, steal_planet_ID, strongest_planet.num_ships / 2)
    
    


# Major Improvement: Choose the "strongest" based on proximity to reinforce or attack.