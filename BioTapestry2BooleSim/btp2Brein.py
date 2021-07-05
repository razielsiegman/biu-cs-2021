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
    def get_interaction_num(self):
        return self.interaction_num

def parse_node_id(full_node_id):
    full_node_id = full_node_id.replace(' ','_')
    return full_node_id[full_node_id.find(':')+1:]

def main():
    edge_set = set()
    sif_filename = input('Enter .sif filename: ')

    # iterate through .sif file
    with open(sif_filename, 'r') as f:
        for line in f.readlines():
            # parse the .sif line as an edge.
            # format is 'nodeID1 [tab] [PROMOTES | REPRESSES | REGULATES] [tab] nodeID2'
            tokens = line.split('\t')
            from_node = parse_node_id(tokens[0])
            interaction_str = tokens[1].rstrip()
            to_node = parse_node_id(tokens[2]).rstrip() # remove newline char
            print(tokens[1])
            brein_format_interaction = 'positive' if (tokens[1] == 'PROMOTES') else 'negative'
            edge = Edge(from_node, to_node, brein_format_interaction)
            edge_set.add(edge)

    with open('output_'+sif_filename, 'w') as f:
        text = ''
        for edge in edge_set:
            text += '{}\t{}\t{};\n'.format(edge.get_from_node(), edge.get_to_node(), edge.interaction)
        f.write(text.rstrip())

main()