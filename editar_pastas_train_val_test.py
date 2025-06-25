'''
import os
import random
import shutil

# Diretórios de origem
base_dir = os.path.dirname(__file__)
dir_images = os.path.join(base_dir, 'images_augmented')
dir_labels = os.path.join(base_dir, 'labels_augmented')

# Diretório base de saída
output_base = os.path.join(base_dir, 'data')

# Pastas de saída
subsets = ['train', 'val', 'test']
for subset in subsets:
    os.makedirs(os.path.join(output_base, subset, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_base, subset, 'labels'), exist_ok=True)

# Listar imagens com labels correspondentes
imagens = [f for f in os.listdir(dir_images) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
imagens_com_label = [f for f in imagens if os.path.exists(os.path.join(dir_labels, os.path.splitext(f)[0] + '.txt'))]

# Embaralhar aleatoriamente
random.shuffle(imagens_com_label)

# Dividir: 70% treino, 20% validação, 10% teste
total = len(imagens_com_label)
n_train = int(total * 0.7)
n_val = int(total * 0.2)
n_test = total - n_train - n_val  # garante 100%

train_files = imagens_com_label[:n_train]
val_files = imagens_com_label[n_train:n_train + n_val]
test_files = imagens_com_label[n_train + n_val:]

# Função auxiliar para copiar imagens e labels
def copiar(lista_arquivos, subset):
    for nome_img in lista_arquivos:
        nome_base, ext = os.path.splitext(nome_img)
        origem_img = os.path.join(dir_images, nome_img)
        origem_lbl = os.path.join(dir_labels, nome_base + '.txt')

        destino_img = os.path.join(output_base, subset, 'images', nome_img)
        destino_lbl = os.path.join(output_base, subset, 'labels', nome_base + '.txt')

        shutil.copyfile(origem_img, destino_img)
        shutil.copyfile(origem_lbl, destino_lbl)

# Executar cópias
copiar(train_files, 'train')
copiar(val_files, 'val')
copiar(test_files, 'test')

# Resumo
print(f'Treinamento: {len(train_files)} imagens')
print(f'Validação: {len(val_files)} imagens')
print(f'Teste: {len(test_files)} imagens')
print('Separação concluída.')
'''