from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests


GUI = Builder.load_file("main.kv")
class MainApp(App):
    id_usuario = 1

    def build(self):
        return GUI
    
    def on_start(self):
        requisition = requests.get(f"https://app-basic-12d09-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisition_dict = requisition.json()
        avatar = requisition_dict['avatar']
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"
    
    def mudar_tela(self, id_tela):
        print(id_tela)
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela


MainApp().run()