from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)

def encontrar_faixa_azul(imagem, cor_alvo, tolerancia_cor=60, margem_erro=4): 
    """
    Encontra as linhas divisórias reais exigindo continuidade horizontal (mínimo 100px),
    evitando que letras e textos normais causem cortes falsos.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # ALTERAÇÃO MÍNIMA: Definição do intervalo exato pedido por você
    x_inicio = 326
    comprimento_exigido = 612  # Percorre de 326 até 938 (938 - 326 = 612)
    
    y = 0
    while y < altura:
        # ALTERAÇÃO MÍNIMA: Substituição do bloco vertical pela varredura horizontal de 612px
        extensao_horizontal = 0
        for dx in range(comprimento_exigido):
            if x_inicio + dx >= largura:
                break
            r, g, b = pixels[x_inicio + dx, y][:3]
            if abs(r - 0) <= tolerancia_cor and abs(g - 0) <= tolerancia_cor and abs(b - 0) <= tolerancia_cor:
                extensao_horizontal += 1
            else:
                break
        
        # Quando der os 612 pixels pretos contínuos, ele entra aqui e corta
        if extensao_horizontal >= comprimento_exigido:
            posicao_corte = y - 15  
            if posicao_corte < 0:  
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Linha REAL de questão validada em y={y} (Extensão horizontal: {extensao_horizontal}px). Cortando em y={posicao_corte}")
            
            # Salta uma margem para sair totalmente da hachura
            y += 40
            continue
                
        y += 1
    
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente cortando ANTES das faixas
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_azul(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão real de questão encontrado na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} linhas reais para corte")
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        posicao_anterior = posicao_corte
    
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    #caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Substitua pelo caminho da sua imagem
    #pasta_saida = "questoes_colunas" # Substitua pelo nome da pasta de saída desejada (questoes_colunas, pagina_15, pagina_28)

    caminho_imagem = "./inteira/pagina_enem_31.png"  # Substitua pelo caminho da sua imagem
    pasta_saida = "pagina_31" # Substitua pelo nome da pasta de saída desejada (questoes_colunas, pagina_15, pagina_28)
    
 
    
    cor_do_padrao = converter_cor_gimp_para_rgb(0.0, 0.0, 0.0) 
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída!")
