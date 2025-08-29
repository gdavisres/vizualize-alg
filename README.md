# Projeto: Visualização e Benchmark de Algoritmos de Ordenação

Projeto educativo para implementar, visualizar e medir a eficiência de algoritmos de ordenação.

## Algoritmos implementados
- Bubble Sort
- Insertion Sort
- Selection Sort
- Merge Sort
- Quick Sort

## Requisitos
Veja [`requirements.txt`](requirements.txt:1) para dependências.

- Python 3.8+

### Instalação rápida (sem venv)

A seguir há instruções para instalar as dependências e executar o projeto diretamente a partir da cópia do repositório do GitHub, sem usar ambientes virtuais.

- Windows (instalação por usuário):
```bash
# use o executável python instalado no sistema
python -m pip install --user -r requirements.txt
```

- macOS / Linux (instalação por usuário):
```bash
# em muitos sistemas o executável é python3
python3 -m pip install --user -r requirements.txt
# ou, se preferir instalar globalmente (requer sudo):
# sudo python3 -m pip install -r requirements.txt
```

Observações:
- O parâmetro --user instala os pacotes apenas para o usuário atual e evita necessidade de permissões de administrador.
- Se o comando python ou python3 não for reconhecido, use o caminho completo para o executável Python do sistema ou ajuste o PATH.
- Em Windows, caso os scripts não estejam no PATH após instalação com --user, execute os scripts chamando explicitamente `python arquivo.py`.

## Executando testes unitários
```bash
# Windows/macOS/Linux (use python ou python3 conforme seu sistema)
python -m pytest test_sorting.py
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

## Uso rápido (exemplo) — sem venv
```bash
# instale dependências (por usuário)
python -m pip install --user -r requirements.txt

# rodar benchmark
python benchmark_sorting.py

# ou gerar animação para um algoritmo específico
python visualize_sorting.py --alg quick --save
```

## Dependências opcionais
- Para exportar mp4 ou melhorar a exportação de vídeos, instale ffmpeg (p.ex. via apt, brew ou download oficial).
- Se matplotlib não estiver disponível, instale com `python -m pip install --user matplotlib` ou confira `requirements.txt`.

## Licença
MIT License

## Autor
Autor: Gabriel Resende
