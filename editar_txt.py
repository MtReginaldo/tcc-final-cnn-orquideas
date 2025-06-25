import os
import glob

# Diretório base do projeto (onde está este script)
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')

# Subconjuntos e caminhos de saída
subsets = ['train', 'val', 'test']

for subset in subsets:
    image_dir = os.path.join(data_dir, subset, 'images')
    output_txt = os.path.join(base_dir, f'{subset}.txt')

    imagens = sorted(glob.glob(os.path.join(image_dir, '*.*')))

    with open(output_txt, 'w') as f:
        for caminho_img in imagens:
            # Caminho relativo ao projeto, com 'data/' no início
            caminho_relativo = os.path.relpath(caminho_img, base_dir)
            f.write(caminho_relativo.replace('\\', '/') + '\n')  # uso do / para compatibilidade com YOLO

    print(f'{subset}.txt gerado com {len(imagens)} imagens.')
