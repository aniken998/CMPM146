import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

# Simple Attack
def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

# Simple Spread
def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

# Complex Defense Version 1.0
def defend_weakest_ally_planet(state):
    # (1) Find out whether we can safely reinforce. 
    # (a) Find the targetted ally planet.
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)
    # Sort Enemy Fleet from Weakest to Strongest
    # enemy_ships = state.enemy_fleets(), key=lambda p: p.num_ships, default=None
    for fleet in state.enemy_fleets():
        target = fleet.destination_planet
        enemy_units = fleet.num_ships

        # If I have not already done this.
        # Go through current fleets to confirm there is not already something being sent.
        # if target not in state.my_fleets().destination_planet:

        # (2) Get the strongest ally planet
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

        # (3) Get the Travel time to the ally.
        logging.debug(str(strongest_planet))
        logging.debug(str(target))
        deviation = state.distance(strongest_planet.ID, target)
    
        # (4) Calculate Risk factor in sending backup
        if deviation + strongest_planet.num_ships < enemy_units:
            # Too Risky ABORT
            return False
        else:
            return issue_order(state, strongest_planet.ID, weakest_planet.ID, enemy_units + deviation)

    # All allys have reinforcements incoming.
    return False