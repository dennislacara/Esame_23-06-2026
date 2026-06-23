from database.dao import Dao
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._users_list = []
        self.map_users = {}
        self.load_all_users()

        self.users_with_n_bus = []



    def load_all_users(self):
        self._users_list = Dao.read_all_users()
        for user in self._users_list:
            self.map_users[user.user_id] = user
        print(f"Users: {self._users_list}")

    def crea_grafo(self, n_bus):
        self._graph.clear()

        self.users_with_n_bus = Dao.read_users_with_n_bus(n_bus, self.map_users)
        #implemento nodi
        for u in self.users_with_n_bus:
            self._graph.add_node(u.user_id)

        #implemento archi con filtraggio
        spigoli = Dao.read_edges()
        for s in spigoli:
            #aggiungo l'arco solo se i nodi sono presenti nel grafo
            if s.id1 in self._graph.nodes() and s.id2 in self._graph.nodes():
                self._graph.add_edge(s.id1, s.id2, peso = s.comuni)
        n_nodi = self._graph.number_of_nodes()
        n_spigoli = self._graph.number_of_edges()
        print(f'grafo creato: {n_nodi} nodi , {n_spigoli} archi')
        return n_nodi, n_spigoli

    def get_utenti_piu_connessi(self):
        lista = []
        #per ogni nodo del grafo, iterazione sui vicini
        for n in self._graph.nodes():
            connessioni = 0

            for vicino in self._graph.neighbors(n):

                connessioni += self._graph[n][vicino]['peso']

            lista.append((self.map_users[n], connessioni))
        lista.sort(key=lambda tup: tup[1], reverse=True)
        print(f'Lista utenti piu connessi: {lista}')
        return lista


    def get_percorso(self, id_utente, l):

        self.best_path = []
        self.best_value = 0

        self.ricorsione([id_utente], l, 0)

        self.best_path = [self.map_users[id_utente] for id_utente in self.best_path]

        print('Algoritmo ricorsivo eseguito.')
        print(f'Sequenza calcolata: {self.best_path}')
        print(f'Valore ottimo calcolato: {self.best_value}')
        return self.best_path, self.best_value

    def ricorsione(self, parziale, l, valore):

        if len(parziale) == l:
            if valore > self.best_value:
                self.best_value = valore
                self.best_path = parziale.copy()
            return

        for vicino in self._graph.neighbors(parziale[-1]):

            if vicino in parziale:
                continue

            parziale.append(vicino)
            nuovo_valore = valore + self._graph[parziale[-2]][parziale[-1]]['peso']
            self.ricorsione(parziale, l, nuovo_valore)
            parziale.pop()
