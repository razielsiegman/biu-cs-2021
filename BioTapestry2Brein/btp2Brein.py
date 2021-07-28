import xml.etree.ElementTree as ET

# other option is 'dash', or even a tuple of ('dot','dash')
OPTIONAL_STYLES = ('dot', 'dash')


class Edge:
    def __init__(self, fromNode, toNode, interaction, is_optional=False):
        self.fromNode = fromNode
        self.toNode = toNode
        self.interaction = interaction
        self.is_optional = is_optional

    def __str__(self) -> str:
        return '<Edge from {} to {} with interaction={}, optional={}>'.format(
            self.fromNode, self.toNode, self.interaction, self.is_optional)

    def __eq__(self, o) -> bool:
        if isinstance(o, Edge):
            return self.fromNode == o.fromNode and \
                self.toNode == o.toNode and \
                self.interaction == o.interaction and \
                self.is_optional == o.is_optional
        return False

    def __hash__(self) -> int:
        return hash((self.fromNode, self.toNode, self.interaction, self.is_optional))


def parse_node_id(full_node_id):
    full_node_id = full_node_id.replace(' ', '_')
    return full_node_id[full_node_id.find(':')+1:]


def get_edge_set_from_file():
    edge_set = set()
    filename = input('Enter filename: ')
    suffix = filename[filename.rfind('.'):]
    if suffix == '.btp':
        return get_edge_set_with_btp(filename)
    elif suffix == '.sif':
        edge_set = get_edge_set_with_sif(filename)
        if input('Would you like to manually input optional tags [y/n]? ') == 'y':
            manually_enter_optionals(edge_set)
        return edge_set
    else:
        raise Exception('File type "{}" is not supported'.format(suffix))

def get_edge_set_with_sif(sif_filename):
    edge_set = set()

    # iterate through .sif file
    with open(sif_filename, 'r') as f:
        for line in f.readlines():
            # parse the .sif line as an edge.
            # format is 'nodeID1 [tab] [PROMOTES | REPRESSES | REGULATES] [tab] nodeID2'
            tokens = line.split('\t')
            from_node = parse_node_id(tokens[0])
            interaction_str = tokens[1].rstrip()
            to_node = parse_node_id(tokens[2]).rstrip()  # remove newline char
            brein_format_interaction = 'positive' if (
                tokens[1] == 'PROMOTES') else 'negative'
            edge = Edge(from_node, to_node, brein_format_interaction)
            edge_set.add(edge)
    return edge_set


def get_edge_set_with_btp(btp_filename):
    edge_set = set()
    root = ET.parse(btp_filename).getroot()

    node_id_to_name = {}
    ref_to_edge = {}

    # build map of (id -> gene_name)
    for gene in root.iter('gene'):
        attr = gene.attrib
        node_id_to_name[attr['id']] = attr['name']

    # find links and make corresponding edges
    for link in root.iter('link'):
        attr = link.attrib
        from_node_name = node_id_to_name[attr['src']]
        to_node_name = node_id_to_name[attr['targ']]
        interaction = 'positive' if attr['sign'] == '+' else 'negative'
        edge = Edge(from_node_name, to_node_name, interaction)
        ref_to_edge[attr['id']] = edge
        edge_set.add(edge)

    # update edges to reflect optional/mandatory status
    for node in root.findall(".//drop[perLinkDrawStyle]"):
        style = node[0][0].attrib['style']
        edge = ref_to_edge[node.attrib['ref']]
        if style in OPTIONAL_STYLES:
            edge.is_optional = True

    return edge_set


def extract_nodes_from_edge_set(edge_set: set):
    node_set = set()
    for edge in edge_set:
        node_set.add(edge.fromNode)
        node_set.add(edge.toNode)
    return node_set


def get_rc_text_one_by_one(node_set):
    rc_text = ''
    for node in node_set:
        rc_text += '{}[{}]({}); '.format(
            node,
            input('Enter (+-) for {}: '.format(node)),
            input('Enter regulatory conditions for {}: '.format(node))
        )
    return rc_text

def rcspec_to_oneline(lines):
    oneline = ''
    for line in lines:
        tokens = line.split('\t')
        if len(tokens) < 2: continue
        gene = tokens[0]
        rc = tokens[1].rstrip()
        oneline += '{}[]({}); '.format(gene, rc)
    return oneline

def manually_enter_optionals(edge_set):
    for edge in edge_set:
        if input('Should {} be optional [y/n]? '.format(str(edge))) == 'y':
            edge.is_optional = True


def get_directive_text():
    return 'directive updates {};\ndirective length {};\ndirective uniqueness {};\ndirective limit {};\ndirective regulation {};\n'.format(
        input('directive updates: '),
        input('directive length: '),
        input('directive uniqueness: '),
        input('directive limit: '),
        input('directive regulation: ')
    )


def get_rc_text(node_set):
    rc_pref = input(
        'How would you like to enter regulatory conditions ["m"=manually, "o"=1-by-1, "f"=rcspec file]? ')
    while (rc_pref not in ('m', 'o', 'f')):
        print('***Invalid response to prompt: only "m" and "o" are acceptable...')
        rc_pref = input('How would you like to enter regulatory conditions ["m" for manually, "o" for one-by-one]? ')
    rc_text = ''
    if rc_pref == 'm': rc_text = input('Enter full regulatory conditions specs: ')
    elif rc_pref == 'o': rc_text = get_rc_text_one_by_one(node_set)
    else:
        with open(input('Enter .rcspec filename: '), 'r') as f:
            rc_text = rcspec_to_oneline(f.readlines())
    return rc_text.rstrip() + '\n'

def get_edges_text(edge_set):
    edges_text = ''
    for edge in edge_set:
        edges_text += '{fromNode}\t{toNode}\t{interaction}{opt};\n'.format(
            fromNode=edge.fromNode,
            toNode=edge.toNode,
            interaction=edge.interaction,
            opt='\toptional' if edge.is_optional else '')
    return edges_text


def main():
    edge_set = get_edge_set_from_file()

    directive_text = get_directive_text()
    rc_text = get_rc_text(extract_nodes_from_edge_set(edge_set))
    edges_text = get_edges_text(edge_set)

    with open('model.net', 'w') as f:
        text = directive_text + rc_text + edges_text
        f.write(text.rstrip())


main()
