from model.model import Model
from UI.view import View
import flet as ft

class Controller:
    def __init__(self, view : View, model : Model):
        self._view = view
        self._model = model

    def handler_crea_grafo(self, e):
        try:
            n_bus = int(self._view._txt_nBus.value)
            if n_bus <= 0:
                self._view.show_alert('Inserire un valore positivo. Riprova')
                return
        except Exception:
            self._view.show_alert('Inserire un valore numerico intero positivo. Riprova')
            return
        n_nodi, n_spigoli = self._model.crea_grafo(n_bus)
        self._view._lst_result.controls.clear()
        self._view._lst_result.controls.append(ft.Text(f'Grafo creato correttamente. Nodi {n_nodi} - Archi {n_spigoli}'))

        # accensione bottoni
        self.accensione()

        #incremento dd
        self.populate_dd()

        self._view.update_page()

    def handler_utenti_connessi(self, e):

        lista_utenti = self._model.get_utenti_piu_connessi()
        self._view._lst_result.controls.clear()
        for tupla in lista_utenti:
            self._view._lst_result.controls.append(ft.Text(f'{tupla[0]} - strenght = {tupla[1]}'))
        self._view.update_page()

    def accensione(self):
        self._view._btnUtentiConnessi.disabled = False
        self._view._ddUtente.disabled = False
        self._view._txtL.disabled = False
        self._view._btnSequenza.disabled = False

    def populate_dd(self):
        self._view._ddUtente.options.clear()
        for n in self._model._graph.nodes():
            user = self._model.map_users[n]
            self._view._ddUtente.options.append(ft.dropdown.Option(key = user.user_id, text = user.name))

    def handler_sequenza(self, e):
        try:
            l = int(self._view._txtL.value)
            l_max = len(self._model._graph.nodes())
            if l < 2 or l > l_max:
                if l_max == 0 or l_max == 1:
                    self._view.show_alert('Numero di nodi sotto soglia. Riprova')
                else:
                    self._view.show_alert(f'Inserire un valore compreso tra 2 e {l_max}. Riprova')
                return
        except Exception:
            self._view.show_alert('Inserire un valore numerico intero per la lunghezza. Riprova')
            return

        id_utente = self._view._ddUtente.value
        if id_utente is None:
            self._view.show_alert('Scegliere un utente. Riprova')
            return

        percorso, valore = self._model.get_percorso(id_utente, l)

        self._view._lst_result.controls.clear()
        self._view._lst_result.controls.append(ft.Text(f'Punteggio totale = {valore}'))
        self._view._lst_result.controls.append(ft.Text(f'Sequenza trovata:'))
        for utente in percorso:
            self._view._lst_result.controls.append(ft.Text(f'{utente}'))

        self._view.update_page()
