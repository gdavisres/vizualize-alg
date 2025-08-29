# Projeto: Visualização e Benchmark de Algoritmos de Ordenação

Projeto educativo para implementar, visualizar e medir a eficiência de algoritmos de ordenação.

## Algoritmos implementados
- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort

## Requisitos
Veja [`requirements.txt`](requirements.txt) para dependências.

- Python 3.8+

### Instalação rápida
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Executando testes unitários
```bash
pytest test_sorting.py
```

## Benchmark e gráfico
```bash
python benchmark_sorting.py
```
O benchmark gera um arquivo `sorting_performance.png` no diretório do projeto.

## Gerar/visualizar animações
```bash
python visualize_sorting.py --alg bubble --save
```
Os gifs são salvos como `sorting_animation_{alg}.gif` (ex.: `sorting_animation_bubble.gif`).

## Formatos de saída e métricas
- comparisons: número de comparações realizadas pelo algoritmo.
- swaps: número de trocas entre elementos.
- time_seconds: tempo total em segundos para a execução do algoritmo.

## Uso rápido (exemplo)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python benchmark_sorting.py
```

## Dependências opcionais
- Para exportar mp4 ou melhorar a exportação de vídeos, instale ffmpeg (p.ex. via apt, brew ou download oficial).
- Se matplotlib não estiver disponível, instale com `pip install matplotlib` ou confira `requirements.txt`.

## Licença
MIT License

## Autor
Autor: Gabriel Resende

## Ferramentas
Roo Code + gpt-5-mini
