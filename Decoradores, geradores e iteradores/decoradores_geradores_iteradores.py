### Decoradores

# def duplicar(func):
#     def envelope(*args, **kwargs):
#         func(*args, **kwargs)
#         return func(*args, **kwargs)
        
#     return envelope

# @duplicar
# def aprender(tecnologia):
#     print(f"Estou aprendendo {tecnologia}")
#     return tecnologia.upper()


# tecnologia = aprender("Python")
# print(tecnologia)

# def meu_decorador(funcao):
#     print("meu_decorador")
#     def envelope(*args,**kwargs):
#         print("envelope")
#         print("Faz algo antes de executar")
#         resultado = funcao(*args, **kwargs)
#         print("Faz algo depois de executar")
#         print(f"Resultado = {resultado}")
#         return resultado
#     print('meu_decorador 2')
#     return envelope

# @meu_decorador
# def ola_mundo(nome, outro_argumento):
#     print(f"Olá mundo {nome}!")
#     return nome.upper()


# resultado = ola_mundo("João", 1000)
# print(resultado)
# print(ola_mundo.__name__)

### Introspecção

# import functools

# def duplicar(func):
#     @functools.wraps(func)
#     def envelope(*args, **kwargs):
#         func(*args, *kwargs)
#         return func(*args, *kwargs)
    
#     return envelope

# @duplicar
# def aprender(tecnologia):
#     print(f"Estou aprendendo {tecnologia}")
#     return tecnologia.upper()


# print(aprender.__name__)

### Iterador

# class MeuIterador:
#     def __init__(self, numeros: list[int]):
#         self.numeros = numeros
#         self.contador = 0
        
#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         try:
#             numero = self.numeros[self.contador]
#             self.contador += 1
#             return numero * 2
#         except IndexError:
#             raise StopIteration
    

# for i in MeuIterador(numeros=[28, 12, 16]):
#     print(i)


### Geradores

# # import requests

# # def fetch_products(api_url, max_pages=100):
# #     page = 1
# #     while page <= max_pages:
# #         response =  requests.get(f"{api_url}?page={page}")
# #         data = response.json()
# #         for product in data['products']:
# #             yield product
# #         if 'next_page' not in data:
# #             break
# #         page += 1
        

# # # Uso do gerador
# # for product in fetch_products("http://api.example/products"):
# #     print(product['name'])

def meu_gerador(numeros: list[int]):
    for numero in numeros:
        yield numero * 2

for i in meu_gerador(numeros=[1, 2, 3]):
    print(i)
