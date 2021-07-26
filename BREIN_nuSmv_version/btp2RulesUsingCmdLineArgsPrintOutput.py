import pprint as pp
from sympy.logic.boolalg import *
from sympy import *
import sys

DEFAULT_RC_SPEC = '0' # chose randomly
EXPORT_TYPE = ''

'''
CLASSES 
'''
class Edge:
    def __init__(self, fromNode, toNode, interaction):
        self.fromNode = fromNode
        self.toNode = toNode
        self.interaction = interaction

    def __str__(self) -> str:
        return '<Edge from {} to {} with interaction={}>'.format(self.fromNode, self.toNode, self.interaction)

    def get_from_node(self):
        return self.fromNode
    def get_to_node(self):
        return self.toNode
    def get_interaction(self):
        return self.interaction

'''
HELPER METHODS
'''
#TODO still unfinished, check btp docs
def parse_node_id(full_node_id):
    full_node_id = full_node_id.replace(' ','_')
    return full_node_id[full_node_id.find(':')+1:]

# translate from python boolean-logic syntax to BooleSim/BoolNet readable syntax
def clean_bool_expression(bool_expression):
    if EXPORT_TYPE == 'bs':
        return bool_expression.replace('&','&&').replace('|','||').replace('~','!')
    elif EXPORT_TYPE == 'bn':
        return bool_expression.replace('~','!')

# takes in regulatory conditions specifications, along with the interactions of the node, 
# and translates those into a boolean expression readable by BooleSim  
def generate_bool_expression(rc_spec, incoming_edges):
    bool_expression = symbols('false') # arbitrary init
    
    # AllActivators AND NoRepressors
    if rc_spec == '0':
        bool_expression = And(all_activators_expr(incoming_edges), no_repressors_expr(incoming_edges))
    
    # NOT NoActivators AND NoRepressors
    elif rc_spec == '1':
        bool_expression = And(Not(no_activators_expr(incoming_edges)),no_repressors_expr(incoming_edges))
    
    # AllActivators AND NOT AllRepressors
    elif rc_spec == '2':
        bool_expression = And(all_activators_expr(incoming_edges),Not(all_repressors_expr(incoming_edges)))
    
    # (NoRepressors AND NOT NoActivators) OR (NOT AllRepressors AND AllActivators)
    elif rc_spec == '3':
        lhs = And(no_repressors_expr(incoming_edges),Not(no_activators_expr(incoming_edges)))
        rhs = And(Not(all_repressors_expr(incoming_edges)),all_activators_expr(incoming_edges))
        bool_expression = Or(lhs,rhs)
    
    # AllActivators
    elif rc_spec == '4':
        bool_expression = all_activators_expr(incoming_edges)
    
    # AllActivators OR (NoRepressors AND NOT NoActivators)
    elif rc_spec == '5':
        lhs = all_activators_expr(incoming_edges)
        rhs = And(no_repressors_expr(incoming_edges),Not(no_activators_expr(incoming_edges)))
    
    # NOT NoActivators AND NOT AllRepressors
    elif rc_spec == '6':
        bool_expression = And(Not(no_activators_expr(incoming_edges)), Not(all_repressors_expr(incoming_edges)))
    
    # (NOT NoActivators AND NOT AllRepressors) OR AllActivators
    elif rc_spec == '7':
        bool_expression = Or(And(no_activators_expr(incoming_edges) , Not(all_repressors_expr(incoming_edges))), all_activators_expr(incoming_edges))
    
    # NOT NoActivators
    elif rc_spec == '8':
        bool_expression = Not(no_activators_expr(incoming_edges))
    
    # NoRepressors
    elif rc_spec == '9':
        bool_expression = no_repressors_expr(incoming_edges)
    
    # NoRepressors OR (NOT AllRepressors AND AllActivators)
    elif rc_spec == '10':
        lhs = no_repressors_expr(incoming_edges)
        rhs = And(Not(all_repressors_expr(incoming_edges)),all_activators_expr(incoming_edges))
        bool_expression = Or(lhs, rhs)
    
    # NoRepressors OR (NOT NoActivators AND NOT AllRepressors)
    elif rc_spec == '11':
        bool_expression = Or(no_repressors_expr(incoming_edges), And(Not(no_activators_expr(incoming_edges)), Not(all_repressors_expr(incoming_edges))))
    
    # NOT AllRepressors
    elif rc_spec == '12':
        bool_expression = Not(all_repressors_expr(incoming_edges))
    
    # NoRepressors OR AllActivators
    elif rc_spec == '13':
        bool_expression = Or(no_repressors_expr(incoming_edges), all_activators_expr(incoming_edges))
    
    # (NoRepressors OR AllActivators) OR (NOT AllRepressors AND NOT NoActivators)
    elif rc_spec == '14':
        bool_expression = Or(Or(no_repressors_expr(incoming_edges), all_activators_expr(incoming_edges)), Or(Not(all_repressors_expr(incoming_edges)), Not(no_activators_expr(incoming_edges))))
    
    # NOT AllRepressors OR AllActivators
    elif rc_spec == '15':
        bool_expression = Or(Not(all_repressors_expr(incoming_edges)), all_activators_expr(incoming_edges))
    
    # NoRepressors OR NOT NoActivators
    elif rc_spec == '16':
        bool_expression = Or(no_repressors_expr(incoming_edges), Not(no_activators_expr(incoming_edges)))
    
    # NOT AllRepressors OR NOT NoActivators
    elif rc_spec == '17':
        bool_expression = Or(Not(all_repressors_expr(incoming_edges)), Not(no_activators_expr(incoming_edges)))

    bool_expression = simplify_logic(str(bool_expression))
    return clean_bool_expression(str(bool_expression))

'''
Shortcut methods to retrieve the 4 basic expressions
'''
def all_activators_expr(incoming_edges):
    activator_nodes = get_activator_nodes(incoming_edges)
    bool_expression = symbols('true')
    for i in range(len(activator_nodes)):
        bool_expression = And(bool_expression,symbols(activator_nodes[i]))
    return bool_expression

def no_activators_expr(incoming_edges):
    activator_nodes = get_activator_nodes(incoming_edges)
    bool_expression = symbols('true')
    for i in range(len(activator_nodes)):
        bool_expression = And(bool_expression,Not(symbols(activator_nodes[i])))
    return bool_expression

def all_repressors_expr(incoming_edges):
    repressor_nodes = get_repressor_nodes(incoming_edges)
    bool_expression = symbols('true')
    for i in range(len(repressor_nodes)):
        bool_expression = And(bool_expression,symbols(repressor_nodes[i]))
    return bool_expression

def no_repressors_expr(incoming_edges):
    repressor_nodes = get_repressor_nodes(incoming_edges)
    bool_expression = symbols('true')
    for i in range(len(repressor_nodes)):
        bool_expression = And(bool_expression,Not(symbols(repressor_nodes[i])))
    return bool_expression

def get_activator_nodes(incoming_edges):
    activator_nodes = []
    for edge in incoming_edges:
        if edge.get_interaction() == 'PROMOTES': activator_nodes.append(edge.get_from_node())
    return activator_nodes

def get_repressor_nodes(incoming_edges):
    repressor_nodes = []
    for edge in incoming_edges:
        if edge.get_interaction() == 'REPRESSES': repressor_nodes.append(edge.get_from_node())
    return repressor_nodes

'''
Main Script
'''
def main():
    # cmd line call is: 
    # python btp2RulesUsingCmdLineArgs.py <export type> <sif filename> <rcspec filename>
    global EXPORT_TYPE
    EXPORT_TYPE = sys.argv[1]
    # init data structures
    node_set = set()
    node_to_incoming_edges = {}
    rc_specs = {}
    rules = {}
    
    sif_filename = sys.argv[2]
    rc_specs_filename = sys.argv[3]

    # iterate through .sif file
    with open(sif_filename, 'r') as f:
        for line in f.readlines():
            # parse the .sif line as an edge. 
            # format is 'nodeID1 [tab] [PROMOTES | REPRESSES | REGULATES] [tab] nodeID2'
            tokens = line.split('\t')
            from_node = parse_node_id(tokens[0])
            interaction_str = tokens[1]
            to_node = parse_node_id(tokens[2]).rstrip() # remove newline char
            edge = Edge(from_node, to_node, interaction_str)
            
            # update (node -> incoming edges) map
            node_set.update([from_node, to_node])
            if to_node in node_to_incoming_edges: node_to_incoming_edges[to_node].add(edge)
            else: node_to_incoming_edges[to_node] = {edge}

    # initialize default rc's for each node
    for node in node_set:
        rc_specs[node] = DEFAULT_RC_SPEC
    
    # iterate through rc_specs and parse
    with open(rc_specs_filename, 'r') as f:
        for line in f.readlines():
            tokens = line.split('\t')
            node_id = tokens[0]
            rc_spec = tokens[1].rstrip()
            rc_specs[node_id] = rc_spec

    # generate  rules for all nodes, using the rc_specs
    for node, incoming_edges in node_to_incoming_edges.items():
        rules[node] = generate_bool_expression(rc_specs[node], incoming_edges)
    
    text = ''
    for node, rule in rules.items():
        text += '{} = {}\n'.format(node, rule)
    print(text)

main()


