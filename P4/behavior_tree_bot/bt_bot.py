#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    
    # defense_planet = Sequence(name='Save My Planet')
    # check_attack = Check(if_planet_got_attack)
    # protect = Action(protect_planet)
    # defense_planet.child_nodes = [check_attack, protect]

    # silent = Sequence(name="do nothing")
    # check_ships = Check(check_ship_left)
    # wait = Action(do_no_op)
    # silent.child_nodes = [check_ships, wait]

    defensive_plan = Sequence(name='Deffensive Strategy')
    check_owned_ship = Check(have_more_conquest)
    protect_action = Action(defendPlanet)
    defensive_plan.child_nodes = [check_owned_ship, protect_action]
    # defense = Selector(name='defense')
    # defense.child_nodes = [denfensive_plan]

    populate_plan = Sequence(name='no-op')
    conserve_check = Check(save_fleet)
    nothing = Action(do_no_op)
    populate_plan.child_nodes = [conserve_check, nothing]

    growth_plan = Sequence(name='Eco Strategy')
    eco_check = Check(need_econ)
    grow = Action(spread_ally)
    growth_plan.child_nodes = [eco_check, grow]
    
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_less_conquest)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    conquest_check = Check(have_less_conquest)
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [conquest_check, neutral_planet_check, spread_action]

    steal_plan = Sequence(name='Thief')
    steal_check = Check(steal_fleet)
    big_check = Check(have_largest_fleet)
    steal = Action(steal_planet)
    steal_plan.child_nodes = [big_check, steal_check, steal]

    '''
    defensive_plan = Sequence(name='Defend Strategy')
    enemy_planet_attack_check = Check(if_enemy_planet_attack)
    largest_fleet_check = Check(have_largest_fleet)
    visiting_check = Check(is_busy_reinforce) # Returns true if already did this.
    '''

    #steal and growth plan could cause a lost
    #root.child_nodes = [spread_sequence, offensive_plan, defensive_plan, steal_plan]
    root.child_nodes = [defensive_plan, offensive_plan, spread_sequence, steal_plan]
    
    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
