from requests import post, Session
from json import JSONDecodeError
from requests import get
from bs4 import BeautifulSoup
from time import sleep


class OmieBase:
    def __init__(self, omie_app_key: str, omie_app_secret: str, session: bool=False):
        """
        :param omie_app_key:              Chave api da omie
        :param omie_app_secret:           APi Secret da omie
        """
        self._endpoint = 'https://app.omie.com.br/api/v1/'
        self._appkey = omie_app_key
        self._appsecret = omie_app_secret
        self._head = {'Content-type': 'application/json'}
        self._has_session = False
        
        if session:
            self._session = Session()

    def _gerar_json(self, call: str, param: dict | tuple | list) -> dict:
        return {
            "call": call,
            "app_key": self._appkey,
            "app_secret": self._appsecret,
            "param": [param]
        }

    def _post_request(self, url: str, json: dict) -> dict:
            try:
                if self._has_session:
                    r = self._session.post(url, headers=self._head, json=json)
                else:
                    while True:
                        r = post(url, headers=self._head, json=json)
                        if r.status_code != 400:
                            break
                        sleep(1)
                
                if r.status_code == 200:
                    try:
                        return r.json()
                    except JSONDecodeError as erro:
                        return {
                            'Error': 'JSON Decode Error',
                            'Message': f'{erro}'
                        }
                
                else:
                    return {
                        'Error': r.status_code,
                        'headers':  r.headers,
                        'Mensagem': r.json()
                    }
                    
            except Exception as erro:
                return {
                        'Error': 'Erro ao fazer requisição ',
                        'Mensagem': f'{erro}'
                    }
            
    def _chamar_api(self, endpoint: str = None, call: str = None, param: dict | tuple | list = None) -> dict:
        """
        :keyword endpoint:         Final da url EX: geral/contacorrente/
        :keyword call:             Chamada para api  EX: ListarContasCorrentes
        :keyword param:            Parametros para a chamada
                                   Ex:{"pagina": 1, "registros_por_pagina": 100, "apenas_importado_api": "N"}

        :return:                 Resultado da Requisição ou erro
        """
        url = f'{self._endpoint}{endpoint}'
        json = self._gerar_json(call, param)
        return self._post_request(url, json)

    # @property
    # def endpoint_api(self):
    #     """ Metodo que busca online todos os endpoints da api """
    #     return [link.replace('https://app.omie.com.br/api/v1/') for link in self.pega_links_api()]

    # def conectar_api(self, metodo: str, endpoint: str, parametros: dict) -> dict:
    #     """
    #      ##> Metdodo geral para chamar a api
    #      > Para usar este metodo tenha como referencia a documentação oficial do omie
    #      > link: https://developer.omie.com.br/

    #     :param metodo:       Função a ser realizada disponivel na api omie EX:  'AssociarCodIntServico'
    #     :param endpoint:     Endpiot url da api EX:      'servicos/servico/'
    #     :param parametros:   Parametros usados na requisição, EX:  { "nCodServ": 0, "cCodIntServ": "" }
    #     :return: Retorna dicionario com resultados da requisição ou erro, erros com Tipos Complexos são gerenciados pela
    #     api.
    #     """
    #     return self._chamar_api(
    #         call=metodo,
    #         endpoint=endpoint,
    #         param=parametros
    #     )
    
    # # Extraída a função pega_links_api do módulos scripts.scrap
    # def pega_links_api():
    #     """ Captura todos os links da api atravez do link """
    #     def retquest_devpageomie() -> BeautifulSoup:
    #         try:
    #             r = get('https://developer.omie.com.br/service-list/')
    #             r.raise_for_status()
    #             return BeautifulSoup(r.text, features="html.parser")
    #         except:
    #             raise Exception('Erro na requisição')
    #     suop = retquest_devpageomie().find('div', {'class': 'service-list'})
    #     return {
    #         item.get_text().strip(): item.get("href")
    #         for item in suop.find_all('a')
    #     }

    # def _gerencia_metodo(self, lista_de_metodos: list, metodo: str) -> None:
    #     if metodo not in lista_de_metodos:
    #         raise ValueError(f'{metodo} Não existe!')

    # @staticmethod
    # def _bool_para_sn(boolean: bool) -> str:
    #     return 'S' if boolean else 'N'

    # def _listar_padrao(
    #         self, call: str, endpoint: str, pagina: int, registros_por_pagina: int, apenas_importado_api: bool
    # ) -> dict:
    #     apenas_importado_api = self._bool_para_sn(apenas_importado_api)
    #     return self._chamar_api(
    #         call=call,
    #         endpoint=endpoint,
    #         param={
    #             "pagina": pagina,
    #             "registros_por_pagina": registros_por_pagina,
    #             "apenas_importado_api": apenas_importado_api
    #         }
    #     )

