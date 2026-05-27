# Projeto - Analise de dados

## Resumo do Problema

Este projeto visa construir um pipeline de ETL para o dataset 'Fuel Economy Data: How Efficient Are Today’s Cars?' e desenvolver modelos preditivos para estimar o consumo combinado de combustível de veículos. O objetivo é transformar dados brutos em um modelo dimensional (Star Schema) e, em seguida, utilizar esses dados processados para treinar e avaliar modelos de regressão, comparando seus desempenhos para identificar o mais adequado para a previsão do consumo de combustível.

## 👥 Equipe
* **Ivan Luiz Picolotte dos Santos** - RA: 082210015
* **Rafael Yukio Ivasa** - RA: 082210011 

## Tabela Comparativa de Modelos

Abaixo está a tabela comparativa dos modelos de regressão testados, incluindo suas métricas de desempenho e tempo de processamento:
 
|index|Modelo|MAE|MSE|RMSE|R²|Tempo de Processamento \(s\)|
|---|---|---|---|---|---|---|
|1|Random Forest Regressor|0\.008572746441750136|0\.011927925672113862|0\.10921504325006634|0\.9997053324579627|146\.71464037895203|
|0|Regressão Linear|0\.22302377672242876|0\.09765839950482061|0\.31250343918878815|0\.9975874463563548|35\.479689598083496|

## Modelo Final Escolhido

Com base na análise das métricas de desempenho, o **Random Forest Regressor** foi escolhido como o modelo final para produção. Embora tenha um tempo de treinamento mais longo, ele demonstrou um desempenho significativamente superior em todas as métricas avaliadas (MAE, MSE, RMSE e R²), indicando uma capacidade preditiva muito maior para o consumo combinado de combustível. Seu alto R² (próximo de 1) sugere que ele explica uma grande parte da variância da variável alvo, tornando-o mais robusto e preciso para as previsões desejadas.

## Instruções de Reprodução

Para reproduzir este projeto, siga os passos abaixo:

1.  **Clone o repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd project_root
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate   # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Kaggle API (para download do dataset):**
    *   Vá para sua conta Kaggle, na seção 'API', e clique em 'Create New API Token'. Isso baixará um arquivo `kaggle.json`.
    *   Mova este arquivo para o diretório `~/.kaggle/` (ou crie-o se não existir).
    *   Defina as permissões corretas: `chmod 600 ~/.kaggle/kaggle.json`.

5.  **Execute o notebook:**
    Abra o notebook `notebooks/nome_do_seu_notebook.ipynb` em um ambiente como Jupyter Notebook ou Google Colab e execute todas as células na ordem.

6.  **Acesse os dados processados e o modelo:**
    Os dados processados e o modelo final estarão salvos nas pastas `data/processed/` e `models/`, respectivamente, no Google Drive (se estiver usando Colab) ou localmente, dependendo da configuração de salvamento.
