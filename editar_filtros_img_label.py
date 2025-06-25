import cv2
import os
import glob
import shutil
import numpy as np

# Diretórios
pasta_imagens = './images'
pasta_labels = './labels'
pasta_saida_imagens = './images_augmented'
pasta_saida_labels = './labels_augmented'

# Criar pastas de saída se não existirem
os.makedirs(pasta_saida_imagens, exist_ok=True)
os.makedirs(pasta_saida_labels, exist_ok=True)

# Funções auxiliares para filtros
def ajustar_brilho_contraste(imagem, brilho=0, contraste=1.0):
    return cv2.convertScaleAbs(imagem, alpha=contraste, beta=brilho)

def aplicar_clahe(imagem):
    lab = cv2.cvtColor(imagem, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    imagem_clahe = cv2.merge((cl,a,b))
    return cv2.cvtColor(imagem_clahe, cv2.COLOR_LAB2BGR)

def aplicar_sepia(imagem):
    kernel_sepia = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia = cv2.transform(imagem, kernel_sepia)
    return np.clip(sepia, 0, 255).astype(np.uint8)

# Filtros desejados
filtros = {
    'gray': lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
    'sketch': lambda img: cv2.cvtColor(cv2.addWeighted(img, 0.5, cv2.cvtColor(cv2.bitwise_not(cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 30, 100)), cv2.COLOR_GRAY2BGR), 0.5, 0.0), cv2.COLOR_BGR2RGB),
    'bright': lambda img: ajustar_brilho_contraste(img, brilho=50),
    'contrast': lambda img: ajustar_brilho_contraste(img, contraste=1.5),
    'sharpen': lambda img: cv2.filter2D(img, -1, np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])),
    'blur': lambda img: cv2.GaussianBlur(img, (5, 5), 0),
    'clahe': lambda img: aplicar_clahe(img),
    'sepia': lambda img: aplicar_sepia(img),
    'negative': lambda img: cv2.bitwise_not(img)
}

# Processar todas as imagens
for caminho_imagem in glob.glob(os.path.join(pasta_imagens, '*.*')):
    if not caminho_imagem.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print(f'Erro ao ler {caminho_imagem}')
        continue

    nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
    extensao = os.path.splitext(os.path.basename(caminho_imagem))[1]

    for prefixo, funcao_filtro in filtros.items():
        imagem_filtrada = funcao_filtro(imagem)

        # Garantir que esteja em 3 canais (BGR) ao salvar
        if len(imagem_filtrada.shape) == 2:
            imagem_filtrada = cv2.cvtColor(imagem_filtrada, cv2.COLOR_GRAY2BGR)

        nome_novo = f'{prefixo}_{nome_base}{extensao}'
        caminho_saida_img = os.path.join(pasta_saida_imagens, nome_novo)
        cv2.imwrite(caminho_saida_img, imagem_filtrada)

        # Copiar a label correspondente
        label_origem = os.path.join(pasta_labels, f'{nome_base}.txt')
        label_destino = os.path.join(pasta_saida_labels, f'{prefixo}_{nome_base}.txt')
        if os.path.exists(label_origem):
            shutil.copy(label_origem, label_destino)
        else:
            print(f'Label não encontrada para {nome_base}.txt')

print('Aumento de dados concluído com sucesso.')
