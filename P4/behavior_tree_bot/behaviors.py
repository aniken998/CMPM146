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
    reinforcements = abs(100 - (weakest_planet - strongest_planet))
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, reinforcements)

# Does nothing. Just gain free econ and sit back.
def do_no_op(state):
    return True