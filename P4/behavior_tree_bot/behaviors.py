import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

# Want to insert a special case to supply planets when their growth exceeds an amount.


# Complex Attack
def attack_weakest_enemy_planet(state):
    # Prereq: Prior Check for Fleets already attacking.

    # (1) If we currently have a fleet in flight, abort plan.
    # Improve: Count all fleets going to an enemy planet. 
    if len(state.my_fleets()) >= 10: # Max 3 on offense.
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Choose the planet that minimizes loss.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    
    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    max_loss = 0
    for target_planet in state.enemy_planets():
        # Calculate the distance between my strongest and the enemies planets.
        # Factor in growth over the distance, and the initial ships.
        deviation = state.distance(target_planet.ID, strongest_planet.ID)
        growth = target_planet.growth_rate + (deviation * 0.1) # Because this increases based on turns too. 
        health = target_planet.num_ships
        
        if (deviation + health) < max_loss:
            weakest_planet = target_planet
            max_loss = deviation + health

    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Attack if you can take the risk. For Enemy vs neutral take bigger risks.
    if (deviation * growth + health) < strongest_planet.num_ships: 
        # # Overall, never send all your ships. it kills econ.
        # Improvements: Factor in growth rate instead of a standard 1/2
        # target_planet.growth_rate + 1
        # Try to leave at least 100 ships.
        send_ships = abs(100 - strongest_planet.num_ships)
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, send_ships)
    else:
        return False


# Complex Spread
def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
#    if len(state.my_fleets()) >= 2:
#        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Choose the planet that minimizes loss.
    weakest_planet = min(state.neutral_planets(), key=lambda t: t.num_ships, default=None)
    
    # (4) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    max_loss = 0
    for target_planet in state.neutral_planets():
        # Calculate the distance between my strongest and the enemies planets.
        # Factor in growth over the distance, and the initial ships.
        deviation = state.distance(target_planet.ID, strongest_planet.ID)
        health = target_planet.num_ships
        
        if (deviation + health) < max_loss:
            weakest_planet = target_planet
            max_loss = deviation + health

    # (4) Check if move is Valid again
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (5) Attack if you can take the risk.
    if (deviation + health) < strongest_planet.num_ships / 2: 
        # # Overall, never send all your ships. it kills econ.
        # Improvements: Make it send at most 50%. Not exactly half.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
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
        return False

    return True

def steal_planet(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    steal_planet = min(state.not_my_planets(), key=lambda t: t.num_ships, default=None).ID\

    if(strongest_planet.num_ships < 50):
        return False
    
    for fleet in state.enemy_fleets(): 
        target = fleet.destination_planet
        # Can steal a planet
        if strongest_planet.num_ships > fleet.num_ships:
            steal_planet = target

        # Chosen a planet to steal, check if it exists
        if (strongest_planet == None) or (steal_planet == None):            
            return False
    return issue_order(state, strongest_planet.ID, steal_planet, strongest_planet.num_ships / 2)
    
    


# Major Improvement: Choose the "strongest" based on proximity to reinforce or attack.