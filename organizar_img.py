import os

# caminho da pasta principal onde estão as subpastas das classes
diretorio_base = './orchids'

# percorrer cada subpasta 
for nome_classe in os.listdir(diretorio_base):
    caminho_classe = os.path.join(diretorio_base, nome_classe)
    
    if os.path.isdir(caminho_classe):
        imagens = os.listdir(caminho_classe)
        imagens.sort()  # ordenacao

        contador = 1
        for nome_arquivo in imagens:
            extensao = os.path.splitext(nome_arquivo)[1].lower()
            if extensao in ['.jpg', '.jpeg', '.png']:
                novo_nome = f"{nome_classe}_{contador:04d}{extensao}"
                caminho_antigo = os.path.join(caminho_classe, nome_arquivo)
                caminho_novo = os.path.join(caminho_classe, novo_nome)
                os.rename(caminho_antigo, caminho_novo)
                contador += 1

print("Renomeação concluída.")