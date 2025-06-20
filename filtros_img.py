# ainda tenho que fazer duplicar as labels 

import cv2
import os
import glob

# diretório base com as imagens
diretorio_base = './orchids_teste_filtro'

# Função para ajustar brilho e contraste
def ajustar_brilho_contraste(imagem, brilho=30, contraste=1.2):
    return cv2.convertScaleAbs(imagem, alpha=contraste, beta=brilho)

imagens_ignoradas = []

# processar todas as imagens da pasta
for caminho_imagem in glob.glob(os.path.join(diretorio_base, '*.*')):
    if not caminho_imagem.lower().endswith(('.jpg', '.jpeg', '.png')):
        imagens_ignoradas.append((caminho_imagem, "Extensão inválida"))
        continue
    
    imagem_original = cv2.imread(caminho_imagem)
    if imagem_original is None:
        imagens_ignoradas.append((caminho_imagem, "Falha ao ler imagem"))
        continue
    
    nome_arquivo = os.path.basename(caminho_imagem)

    # escala de cinza
    imagem_cinza = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(diretorio_base, 'gray_' + nome_arquivo), imagem_cinza)

    # desenho a lápis
    bordas = cv2.Canny(imagem_cinza, 30, 100)
    desenho = cv2.bitwise_not(bordas)
    desenho_colorido = cv2.cvtColor(desenho, cv2.COLOR_GRAY2BGR)
    imagem_desenho = cv2.addWeighted(imagem_original, 0.5, desenho_colorido, 0.5, 0.0)
    cv2.imwrite(os.path.join(diretorio_base, 'sketch_' + nome_arquivo), imagem_desenho)

    # brilho aumentado
    imagem_brilho = ajustar_brilho_contraste(imagem_original, brilho=50, contraste=1.0)
    cv2.imwrite(os.path.join(diretorio_base, 'bright_' + nome_arquivo), imagem_brilho)

    # contraste aumentado
    imagem_contraste = ajustar_brilho_contraste(imagem_original, brilho=0, contraste=1.5)
    cv2.imwrite(os.path.join(diretorio_base, 'contrast_' + nome_arquivo), imagem_contraste)

print('Processamento concluído.')

if imagens_ignoradas:
    print('\nImagens ignoradas:')
    for caminho, motivo in imagens_ignoradas:
        print(f' - {caminho} | Motivo: {motivo}')
else:
    print('Nenhuma imagem foi ignorada.')
