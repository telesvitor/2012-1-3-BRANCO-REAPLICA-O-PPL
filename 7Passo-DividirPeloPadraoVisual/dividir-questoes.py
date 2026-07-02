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
    x_meio = largura // 2
    altura_max_busca = 28
    
    # Comprimento mínimo horizontal que a linha preta deve ter para não ser considerada uma letra (em pixels)
    comprimento_minimo_linha = 100 
    
    y = 0
    while y < altura - altura_max_busca:
        padrao_encontrado_no_centro = False
        altura_total_encontrada = 16
        
        # 1. Procura o padrão vertical no pixel central exato
        pretos_1 = 0
        while y + pretos_1 < altura:
            r, g, b = pixels[x_meio, y + pretos_1][:3]
            if abs(r - 0) <= tolerancia_cor and abs(g - 0) <= tolerancia_cor and abs(b - 0) <= tolerancia_cor:
                pretos_1 += 1
            else:
                break
        
        if 7 - margem_erro <= pretos_1 <= 7 + margem_erro:
            y_brancos = y + pretos_1
            brancos = 0
            while y_brancos + brancos < altura:
                r, g, b = pixels[x_meio, y_brancos + brancos][:3]
                if abs(r - 255) <= tolerancia_cor and abs(g - 255) <= tolerancia_cor and abs(b - 255) <= tolerancia_cor:
                    brancos += 1
                else:
                    break
                    
            if 5 - margem_erro <= brancos <= 5 + margem_erro:
                y_pretos_2 = y_brancos + brancos
                pretos_2 = 0
                while y_pretos_2 + pretos_2 < altura:
                    r, g, b = pixels[x_meio, y_pretos_2 + pretos_2][:3]
                    if abs(r - 0) <= tolerancia_cor and abs(g - 0) <= tolerancia_cor and abs(b - 0) <= tolerancia_cor:
                        pretos_2 += 1
                    else:
                        break
                        
                if 4 - margem_erro <= pretos_2 <= 4 + margem_erro and pretos_2 > 0:
                    padrao_encontrado_no_centro = True
                    altura_total_encontrada = pretos_1 + brancos + pretos_2

        # 2. SE encontrou no centro, CONFIRMA se é uma linha longa ou apenas uma letra/texto
        if padrao_encontrado_no_centro:
            extensao_horizontal = 0
            
            # Varre para a direita a partir do centro procurando continuidade da linha preta
            for dx in range(1, comprimento_minimo_linha):
                r, g, b = pixels[x_meio + dx, y][:3]
                if abs(r - 0) <= tolerancia_cor and abs(g - 0) <= tolerancia_cor and abs(b - 0) <= tolerancia_cor:
                    extensao_horizontal += 1
                else:
                    break
                    
            # Varre para a esquerda a partir do centro procurando continuidade da linha preta
            for dx in range(1, comprimento_minimo_linha):
                r, g, b = pixels[x_meio - dx, y][:3]
                if abs(r - 0) <= tolerancia_cor and abs(g - 0) <= tolerancia_cor and abs(b - 0) <= tolerancia_cor:
                    extensao_horizontal += 1
                else:
                    break
            
            # Se a soma da extensão horizontal for maior ou igual ao mínimo exigido, é uma linha real de questão!
            if extensao_horizontal >= comprimento_minimo_linha:
                # Corta 15 pixels antes de onde a linha começou para dar respiro ao título
                posicao_corte = y - 15  
                if posicao_corte < 0:  
                    posicao_corte = 0
                    
                posicoes_corte.append(posicao_corte)
                print(f"Linha REAL de questão validada em y={y} (Extensão horizontal: {extensao_horizontal}px). Cortando em y={posicao_corte}")
                
                # Salta uma margem maior para sair totalmente da hachura
                y += altura_total_encontrada + 40
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
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  
    pasta_saida = "questoes_colunas" 
    
    cor_do_padrao = converter_cor_gimp_para_rgb(0.0, 0.0, 0.0) 
    
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída!")
