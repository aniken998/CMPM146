
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    #if reaches the target, return that node and state
    if node.untried_actions or not node.child_nodes:
        return node,state
    else:
        # print("I'm in else")
        #get the best node, recursively traverse the tree
        node = best_ucb(node,board,state,identity)
        state = board.next_state(state, node.parent_action)
        # print("current_node found")
        return traverse_nodes(node, board, state, identity)
        
    


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    #if ending, return the node
    if board.is_ended(state):
        # print("expand ended")
        return node,state
    #a random action from this node
    #print("expand")
    random_action = choice(node.untried_actions)
    #remove the action from untried actions because already made the action
    node.untried_actions.remove(random_action)
    ######### update the state ##########
    state = board.next_state(state, random_action)
    ##############################################
    #create the node
    child = MCTSNode(parent=node, parent_action=random_action, action_list=board.legal_actions(state))
    # add child node in the tree
    node.child_nodes[random_action] = child
    return child,state
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    while not board.is_ended(state):
        state = board.next_state(state, choice(board.legal_actions(state)))
    return state


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        node.wins += won
        node.visits += 1
        node = node.parent
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    win_rate = {}
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # update the state along with the node
        node,selected_state = traverse_nodes(node, board, sampled_game, identity_of_bot)
        node,expanded_state = expand_leaf(node,board,selected_state)
        rollout_state = rollout(board,expanded_state)
        point = board.points_values(rollout_state)
        # win or lose? could be a method here
        won = win_lost(point,identity_of_bot)
        backpropagate(node,won)
    #get the node with the highest win rate
    for child in root_node.child_nodes.values():
        win_rate[child] = child.wins / child.visits
    winner = max(win_rate,key=win_rate.get)
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return winner.parent_action
    # make a best choice with maxium ucb values
def best_ucb(node,board,state,identity):
    # a dictionary to store ucb values for children
    ucbs = {}
    for child in node.child_nodes.values():
        #check identity
        win_rate = child.wins/child.visits if identity == board.current_player(state) else 1 - child.wins/child.visits 
        ucbs[child] = win_rate + explore_faction * sqrt(log(child.parent.visits)/child.visits)
    best_child = max(ucbs, key = ucbs.get)
    return best_child

def win_lost(point, identity):
    if point[identity] == 1 :
        won = 1
    elif point[identity] == 0: 
        won = 0
    else:
        won = -1
    return won
