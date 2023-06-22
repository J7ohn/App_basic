from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
from bannervenda import BannerVenda
import requests
import os
from functools import partial


GUI = Builder.load_file("main.kv")
class MainApp(App):
    id_usuario = 1

    def build(self):
        return GUI
    
    # função que ao iniciar o aplicativo: carrega as informações do usuario; carregar fotos de perfil
    def on_start(self):

        # carregar fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids['fotoperfilpage']
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)

        # carrega as informações do usuario
        self.carregar_infos_usuario()
    
    def carregar_infos_usuario(self):
        # pegar informação do usuário
        requisicao = requests.get(f"https://app-basic-12d09-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisicao_dict = requisicao.json()

        # preencher foto de perfil
        avatar = requisicao_dict['avatar']
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # preencher lista de vendas
        try:
            vendas = requisicao_dict['vendas'][1:]
            pagina_homepage = self.root.ids['homepage']
            lista_vendas = pagina_homepage.ids['lista_vendas']
            for venda in vendas:
                banner = BannerVenda(
                    cliente=venda['cliente'],
                    foto_cliente=venda['foto_cliente'],
                    produto=venda['produto'],
                    foto_produto=venda['foto_produto'],
                    data=venda['data'],
                    preco=venda['preco'],
                    quantidade=venda['quantidade'],
                    unidade=venda['unidade']
                )
                
                lista_vendas.add_widget(banner)

        except:
            pass

    # função que muda as telas do app
    def mudar_tela(self, id_tela):
        print(id_tela)
        gerenciador_telas = self.root.ids["screen_manager"]
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args):
        
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        info = f'{{"avatar": "{foto}"}}'
        requisicao = requests.patch(
            f"https://app-basic-12d09-default-rtdb.firebaseio.com/{self.id_usuario}.json",
            data=info
        )
        


MainApp().run()