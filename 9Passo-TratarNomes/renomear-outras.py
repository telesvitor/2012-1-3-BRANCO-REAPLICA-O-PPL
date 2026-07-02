"""
Propósito: Renomear as imagens do padrão parte_0xx.png para questao-xx.png
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe todas as pastas do passo 8 para este passo 9
OBS2: você vai atualizar o nome das imagens para seguir um padrão, mas você vai fazer isso pasta por pasta
OBS3: atualize a linha 15 com o nome da pasta das questões que você vai arrumar
OBS4: ENTENDA muito bem o for da linha 25!!!!!!!!!!!
"""
import os

def renomear_questoes_simples():
    pasta = "1-88" # ATUALIZAR com o nome da pasta das questões que você vai arrumar (ex: 80-90, 15, 28)
    
    if not os.path.exists(pasta):
        print(f"Pasta {pasta} não encontrada!")
        return
    
    # Mapeamento direto dos nomes antigos para os novos
    mapeamento = {}
        
    # Exemplo: parte_00x a parte_00y -> questao-x a questao-y
    for i in range(76, 128+1):    # atualize seu for com o número da primeira imagem "parte_AlgumaCoisa.png" até o número da última imagem "parte_AlgumaCoisa.png" mais 1 da pasta
        antigo = f"parte_{i:03d}.png"
        #novo = f"questao-{i+78}-espanhol.png"  # faça uma conta: se a primeira pagina for 
        #novo = f"questao-{i+78}-ingles.png"
        novo = f"questao-{i-22}.png" # faça uma conta: se o i do teu for está em 2, e precisa virar questão 35, como você transforma 2 em 35? faça a conta e coloque dentro da concatenação
        
        mapeamento[antigo] = novo
    
    # Aplicar o renomeamento
    for antigo, novo in mapeamento.items():
        caminho_antigo = os.path.join(pasta, antigo)
        caminho_novo = os.path.join(pasta, novo)
        
        if os.path.exists(caminho_antigo):
            os.rename(caminho_antigo, caminho_novo)
            print(f"Renomeado: {antigo} -> {novo}")
        else:
            print(f"Arquivo não encontrado: {antigo}")
    
    print("Renomeação concluída!")

# Executar
if __name__ == "__main__":
    renomear_questoes_simples()