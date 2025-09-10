import pandas as pd

dados = [
    {"pedido": 1, "endereco": "Rua A, 100", "valor": 15, "janela_inicio": "08:00", "janela_fim": "09:00"},
    {"pedido": 2, "endereco": "Rua B, 200", "valor": 20, "janela_inicio": "09:30", "janela_fim": "10:30"},
    {"pedido": 3, "endereco": "Rua C, 300", "valor": 10, "janela_inicio": "08:45", "janela_fim": "09:45"},
    {"pedido": 4, "endereco": "Rua D, 400", "valor": 25, "janela_inicio": "10:00", "janela_fim": "11:00"},
]
df = pd.DataFrame(dados)
print(f"df: {df}")
df.to_csv("pedidos_mock.csv", index=False)
