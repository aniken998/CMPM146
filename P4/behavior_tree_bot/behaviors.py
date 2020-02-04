import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

# Want to insert a special case to supply planets when their growth exceeds an amount.

'''
def high_risk_attack_enemy_planet(state):
    # Get a list of the strongest planets.
    strongest_planets = state.my_planets()
    strongest_planets.sort(key=lambda t: t.num_ships)
    
    # Get some enemy planets
    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    issue_order(state, (strongest_planets[0]).ID, (enemy_planets[0]).ID, (enemy_planets[0]).fleet_num_ships + 1)
'''
# Complex Attack
def attack_weakest_enemy_planet(state):
    # Prereq: Prior Check for Fleets already attacking.

    # (1) If we currently have a fleet in flight, abort plan.
    # Improve: Count all fleets going to an enemy planet. 
    # if len(state.my_fleets()) >= 10: # Max 3 on offense.
    #    return False

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
        growth = target_planet.growth_rate + (deviation) # Because this increases based on turns too. 
        health = target_planet.num_ships
        
        if (growth + health) < max_loss:
            weakest_planet = target_planet
            max_loss = growth + health

    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Attack if you can take the risk. For Enemy vs neutral take bigger risks.
    if (max_loss) > strongest_planet.num_ships: 
        # # Overall, never send all your ships. it kills econ.
        # Improvements: Factor in growth rate instead of a standard 1/2
        # target_planet.growth_rate + 1
        return False

    # Improvement: Try to save at least the mean of the enemy ships. OR highest planet
    max_out = sum(fleet.num_ships for fleet in state.enemy_fleets())
    max_in = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # (5) Leave just enough to defend, allow risk in econ to decimate enemy numbers.    
    if max_out > max_in.num_ships:
        estimated_risk = max_out
    else:
        estimated_risk = max_in.num_ships

    if (estimated_risk < strongest_planet.num_ships):
        #attackers = abs(estimated_risk - strongest_planet.num_ships)
        #attackers = abs(100 - strongest_planet.num_ships)
        attackers = abs((max_loss + 1) - strongest_planet.num_ships)
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, attackers)
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
    deviation = 0
    health = 0
    # enemy_visited = [planet for planet in state.neutral_planets()
    #                   if not any(fleet.destination_planet == planet.ID for fleet in state.enemy_fleets())]
    # logging.debug(str(enemy_visited))
    
    # ally_visited = [planet for planet in state.neutral_planets()
    #                   if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]

    for target_planet in state.neutral_planets():
        # Calculate the distance between my strongest and the enemies planets.
        # Factor in growth over the distance, and the initial ships.
        deviation = state.distance(target_planet.ID, strongest_planet.ID)
        health = target_planet.num_ships
        
        # Account for planets already being taken over. This will let the enemy make it easier to steal.
        # if target_planet in enemy_visited:
        #     # Get the number of ships the enemy has sent.

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
def spread_ally(state):
    # (1) Get the highest growth rate planet currently owned.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    weakest_planet = max(state.my_planets(), key=lambda t: t.growth_rate, default=None)
    
    # Make sure the strongest planet is willing to lose some ships.
    if (strongest_planet.num_ships < 100):
        return False

    # # (2) Search for some new planets to grow.
    # for target_planet in state.my_planets():
    #     # Reinforce the strongest planet to have the best growth rate
    #     if target_planet.growth_rate > strongest_planet.growth_rate:
    #         weakest_planet = target_planet

    # (3) Validify the action
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Increase the eco of the ally planet
    # Try to get atleast 100 ships there
    # Improvement: Try to save at least the mean of the enemy ships. OR highest planet
    max_out = sum(fleet.num_ships for fleet in state.enemy_fleets())
    
    max_in = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    
    # (5) Leave just enough to defend, allow risk in econ to decimate enemy numbers.    
    # Error Handler at end of game.
    if (max_in == None):
        estimated_risk = max_out
    elif (max_out > max_in.num_ships):
        estimated_risk = max_out
    else:
        estimated_risk = max_in.num_ships

    if (estimated_risk < strongest_planet.num_ships):
        #reinforcements = abs(estimated_risk - weakest_planet.num_ships)
        #reinforcements = abs(100 - weakest_planet.num_ships)
        reinforcements = abs(estimated_risk - strongest_planet.num_ships)        
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, reinforcements)
    else:
        return False

# Does nothing. Just gain free econ and sit back.
def do_no_op(state):
    return True

# Major Improvement: Choose the "strongest" based on proximity to reinforce or attack.