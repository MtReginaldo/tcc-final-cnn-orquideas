import os
import pandas as pd
from ultralytics import YOLO

def salvar_metricas_globais(run_dir):
    csv_path = os.path.join(run_dir, 'results.csv')
    if os.path.exists(csv_path):
        metrics_df = pd.read_csv(csv_path)
        print("Métricas por época:")
        print(metrics_df.head())

        # Salvar em arquivo separado, se quiser
        metrics_df.to_csv(os.path.join(run_dir, 'metrics_global.csv'), index=False)
        print(f'Métricas globais salvas em {os.path.join(run_dir, "metrics_global.csv")}')
    else:
        print("Arquivo de métricas globais não encontrado.")

def salvar_metricas_por_classe(result_val, run_dir):
    # result_val é o retorno do model.val()
    # Extrair métricas por classe, se disponíveis
    if hasattr(result_val, 'metrics') and result_val.metrics:
        per_class = result_val.metrics.get('per_class', None)
        if per_class:
            df = pd.DataFrame(per_class)
            csv_path = os.path.join(run_dir, 'metrics_per_class.csv')
            df.to_csv(csv_path, index=False)
            print(f'Métricas por classe salvas em {csv_path}')
        else:
            print('Métricas por classe não encontradas no resultado da validação.')
    else:
        print('Resultado da validação não contém métricas detalhadas por classe.')

if __name__ == '__main__':
    # 1) Treinar o modelo
    model = YOLO('yolov8n.yaml')

    results = model.train(
        data='data.yaml',
        epochs=30,
        batch=16,
        imgsz=640,
        verbose=True
    )

    print("Treinamento concluído!")

    # Pegar pasta do run criado pelo treino (padrão)
    run_dir = results.dir if hasattr(results, 'dir') else 'runs/detect/train'

    # 2) Salvar métricas globais do treino
    salvar_metricas_globais(run_dir)

    # 3) Rodar validação para métricas detalhadas por classe
    print('Executando validação final para obter métricas por classe...')
    result_val = model.val(data='data.yaml', imgsz=640, batch=16)

    # 4) Salvar métricas por classe
    salvar_metricas_por_classe(result_val, run_dir)
