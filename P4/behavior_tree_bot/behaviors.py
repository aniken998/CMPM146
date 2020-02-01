import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

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
        deviation = state.distance(target_planet.ID, strongest_planet.ID) * 5
        health = target_planet.num_ships
        
        if (deviation + health) < max_loss:
            weakest_planet = target_planet
            max_loss = deviation + health

    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Attack if you can take the risk. For Enemy vs neutral take bigger risks.
    if (deviation + health) < strongest_planet.num_ships: 
        # # Overall, never send all your ships. it kills econ.
        # Improvements: Factor in growth rate instead of a standard 1/2
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships)
    else:
        return False


# Complex Spread
def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 2:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Choose the planet that minimizes loss.
    weakest_planet = min(state.neutral_planets(), key=lambda t: t.num_ships, default=None)
    
    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    max_loss = 0
    for target_planet in state.neutral_planets():
        # Calculate the distance between my strongest and the enemies planets.
        # Factor in growth over the distance, and the initial ships.
        deviation = state.distance(target_planet.ID, strongest_planet.ID) * 2
        health = target_planet.num_ships
        
        if (deviation + health) < max_loss:
            weakest_planet = target_planet
            max_loss = deviation + health

    # (3) Check if move is Valid
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False

    # (4) Attack if you can take the risk.
    if (deviation + health) < strongest_planet.num_ships / 2: 
        # # Overall, never send all your ships. it kills econ.
        # Improvements: Factor in growth rate instead of a standard 1/2
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    else:
        return False