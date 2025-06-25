from ultralytics import YOLO
import os
import pandas as pd

def salvar_metricas_por_classe(result_val, run_dir):
    if hasattr(result_val, 'metrics') and result_val.metrics:
        per_class = result_val.metrics.get('per_class', None)
        if per_class:
            df = pd.DataFrame(per_class)
            csv_path = os.path.join(run_dir, 'metrics_per_class.csv')
            df.to_csv(csv_path, index=False)
            print(f'Métricas por classe (teste) salvas em {csv_path}')
        else:
            print('Métricas por classe não encontradas.')
    else:
        print('Resultado da avaliação não contém métricas.')

def salvar_metricas_globais(run_dir):
    csv_path = os.path.join(run_dir, 'results.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.to_csv(os.path.join(run_dir, 'metrics_global_test.csv'), index=False)
        print(f'Métricas globais (teste) salvas em {os.path.join(run_dir, "metrics_global_test.csv")}')
    else:
        print('Arquivo de métricas globais não encontrado.')

if __name__ == '__main__':
    # 1. Carregar o modelo treinado
    model = YOLO('runs/detect/train1/weights/best.pt')

    # 2. Avaliar no conjunto de teste
    results_test = model.val(data='data.yaml', split='test', imgsz=640, batch=16)

    # 3. Pasta onde foram salvos os resultados
    test_dir = results_test.save_dir if hasattr(results_test, 'save_dir') else 'runs/detect/test'

    # 4. Salvar métricas por classe do conjunto de teste
    salvar_metricas_por_classe(results_test, test_dir)

    # 5. Salvar métricas globais do conjunto de teste
    salvar_metricas_globais(test_dir)
