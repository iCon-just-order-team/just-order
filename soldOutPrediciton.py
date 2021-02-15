from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

# Costruizione Rete Bayesiana ===================

#Fattore climatico
n_meteo = BbnNode(Variable(0, 'meteo', ['soleggiato', 'nuvoloso', 'pioggia']), [0.48, 0.31, 0.21])
n_temperatura = BbnNode(Variable(1, 'temperatura', ['caldo', 'mite', 'freddo']), [0.45, 0.43, 0.12])
n_fattore_climatico = BbnNode(Variable(2, 'fattore climatico', ['buono', 'pessimo']),
                              [0.79, 0.21, 0.95, 0.05, 0.45, 0.55, 0.81, 0.19, 0.91, 0.09, 0.32, 0.68, 0.12, 0.88,
                               0.05, 0.95, 0.03, 0.97])
#Fattore temporale
n_weekend = BbnNode(Variable(3, 'weekend', ['si', 'no']), [0.285, 0.715])
n_periodo_turistico = BbnNode(Variable(4, 'periodo turistico', ['si', 'no']), [0.167, 0.833])
n_fattore_temporale = BbnNode(Variable(5, 'fattore temporale', ['buono', 'pessimo']),
                              [0.98, 0.02, 0.65, 0.35, 0.82, 0.18, 0.21, 0.79])
#FATTORE ESTERNO
n_fattore_esterno = BbnNode(Variable(6, 'fattore esterno', ['buono', 'pessimo']),
                              [0.97, 0.03, 0.56, 0.44, 0.11, 0.89, 0.02, 0.98])

#Intrattenimento
n_intrattenimento = BbnNode(Variable(7, 'intrattenimento', ['trasmissione evento', 'serata', 'nessuno']),
                              [0.15, 0.04, 0.81])

#Caratteristiche Ristorante
n_cibo = BbnNode(Variable(8, 'cibo', ['buono', 'pessimo']), [0.8, 0.2])
n_staff = BbnNode(Variable(9, 'staff', ['buono', 'pessimo']), [0.9, 0.1])
n_caratteristiche_ristorante = BbnNode(Variable(10, 'caratteristiche ristorante', ['buono', 'pessimo']),
                                [0.9, 0.1, 0.31, 0.69, 0.17, 0.83, 0.01, 0.99])

#FATTORE INTERNO
n_fattore_interno = BbnNode(Variable(11, 'fattore interno', ['buono', 'pessimo']),
                              [0.93, 0.07, 0.45, 0.65, 0.9, 0.1, 0.13, 0.87, 0.83, 0.17, 0.06, 0.94])

#FATTORE DI RIEMPIMENTO
n_riempimento = BbnNode(Variable(12, 'riempimento', ['massimo', 'minimo']),
                              [0.95, 0.05, 0.3, 0.7, 0.42, 0.58, 0.01, 0.99])



# Costruisco l'albero =========================

bbn = Bbn() \
    .add_node(n_meteo) \
    .add_node(n_temperatura) \
    .add_node(n_fattore_climatico) \
    .add_node(n_weekend) \
    .add_node(n_periodo_turistico) \
    .add_node(n_fattore_temporale) \
    .add_node(n_fattore_esterno) \
    .add_node(n_intrattenimento) \
    .add_node(n_cibo) \
    .add_node(n_staff) \
    .add_node(n_caratteristiche_ristorante) \
    .add_node(n_fattore_interno) \
    .add_node(n_riempimento) \
    .add_edge(Edge(n_meteo, n_fattore_climatico, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_temperatura, n_fattore_climatico, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_weekend, n_fattore_temporale, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_periodo_turistico, n_fattore_temporale, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_fattore_climatico, n_fattore_esterno, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_fattore_temporale, n_fattore_esterno, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_intrattenimento, n_fattore_interno, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_cibo, n_caratteristiche_ristorante, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_staff, n_caratteristiche_ristorante, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_caratteristiche_ristorante, n_fattore_interno, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_fattore_esterno, n_riempimento, EdgeType.DIRECTED)) \
    .add_edge(Edge(n_fattore_interno, n_riempimento, EdgeType.DIRECTED))

# convert the BBN to a join tree
join_tree_backup = InferenceController.apply(bbn)


def insert_evidence(join_tree, node_name, option_name, value):
    # insert an observation evidence
    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name(node_name)) \
        .with_evidence(option_name, value) \
        .build()
    join_tree.set_observation(ev)


def print_all_tree(join_tree):
    # print the posterior probabilities
    for node, posteriors in join_tree.get_posteriors().items():
        p = ', '.join([f'{val}={prob:.5f}' for val, prob in posteriors.items()])
        print(f'{node} : {p}')


def print_prediction(join_tree):
    # print the posterior probabilities
    for node, posteriors in join_tree.get_posteriors().items():
        if node == 'riempimento':
            max, min = posteriors.items()
            print(f'[{node} : {max[1]*100:.0f}%]')
            if max[1] < 0.25:
                print("Prevista una bassissima affluenza.\nE' fortemente sconsigliato investire in un numero alto di staff e alimenti.")
            elif max[1] < 0.4:
                print("Prevista una bassa affluenza.\nE' sconsigliato investire in un numero alto di staff e alimenti.")
            elif max[1] < 0.6:
                print("Prevista un'affluenza nella media.\nE' consigliato investire in un numero medio-alto di staff e alimenti.")
            elif max[1] < 0.75:
                print("Prevista un'affluenza medio-alta.\nE' consigliato investire in un numero alto di staff e alimenti.")
            else:
                print("Prevista un'affluenza alta.\nE' fortemente consigliato investire in un numero alto di staff e alimenti.")


def prediction():
    join_tree = join_tree_backup.__copy__()

    while True:
        value = input("Inserire la temperatura corrente: [caldo] [mite] [freddo] [non so]\n$ ")
        if value.lower() in ["caldo", "mite", "freddo", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree,"temperatura", value, 1.0)
            break

    while True:
        value = input("Inserire il meteo corrente: [soleggiato] [nuvoloso] [pioggia] [non so]\n$ ")
        if value.lower() in ["soleggiato", "nuvoloso", "pioggia", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "meteo", value, 1.0)
            break

    while True:
        value = input("E' un giorno del weekend?: [si] [no] [non so]\n$ ")
        if value.lower() in ["si", "no", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "weekend", value, 1.0)
            break

    while True:
        value = input("Siamo in un periodo turistico?: [si] [no] [non so]\n$ ")
        if value.lower() in ["si", "no", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "periodo turistico", value, 1.0)
            break

    while True:
        value = input("E' previsto uno dei seguenti intrattenimenti?: [trasmissione evento] [serata] [nessuno] [non so]\n$ ")
        if value.lower() in ["trasmissione evento", "serata", "nessuno", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "intrattenimento", value, 1.0)
            break

    while True:
        value = input("Come valuteresti il cibo prodotto?: [buono] [pessimo] [non so]\n$ ")
        if value.lower() in ["buono", "pessimo", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "cibo", value, 1.0)
            break

    while True:
        value = input("Come valuteresti lo staff ?: [buono] [pessimo] [non so]\n$ ")
        if value.lower() in ["buono", "pessimo", "non so"]:
            if not(value.lower() == "non so"):
                insert_evidence(join_tree, "staff", value, 1.0)
            break
    #print_all_tree(join_tree)
    print_prediction(join_tree)