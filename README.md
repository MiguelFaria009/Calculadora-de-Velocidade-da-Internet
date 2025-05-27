# Teste de Velocidade da Internet

## Descrição
Este projeto é um script Python que realiza um teste de velocidade da internet, medindo a velocidade de download, upload e ping. Ele utiliza a biblioteca `speedtest-cli` para executar o teste e seleciona automaticamente o servidor mais próximo geograficamente com base no IP externo do usuário, usando geolocalização via API `ipinfo.io`. A interface gráfica, desenvolvida com `tkinter`, exibe os resultados de forma clara e intuitiva, com uma barra de progresso durante o cálculo e a opção de fechar a janela com um botão ou a tecla Enter. No Windows, o prompt do DOS é minimizado automaticamente para uma experiência mais limpa.

## Funcionalidades
- Mede a velocidade de download e upload em Mbps.
- Exibe o ping em milissegundos (ms).
- Interface gráfica com feedback visual durante o teste (mensagem "Calculando..." e barra de progresso).
- Usa geolocalização para selecionar o servidor mais próximo com base no IP externo.
- Minimiza automaticamente o prompt do DOS no Windows.
- Opção de fechar a janela com botão "Fechar" ou tecla Enter.
- Logs detalhados para depuração (exibidos no terminal minimizado).

## Requisitos
- Python 3.x
- Bibliotecas:
  - `speedtest-cli` (instalada via `pip install speedtest-cli`)
  - `requests` (instalada via `pip install requests`, para geolocalização)
  - `pywin32` (opcional, para minimizar o prompt no Windows; instalada via `pip install pywin32`)

## Instalação
1. Clone o repositório ou baixe o arquivo `speed_test.py`:
   ```
   git clone <seu-repositorio>
   ```
2. Instale as dependências necessárias:
   ```
   pip install speedtest-cli
   pip install requests
   pip install pywin32  # Opcional, para minimizar o prompt no Windows
   ```
3. Execute o script:
   ```
   python speed_test.py
   ```

## Uso
- Ao executar o script, uma janela gráfica será aberta imediatamente.
- A mensagem "Calculando..." será exibida enquanto o teste é realizado, acompanhada por uma barra de progresso.
- Após o cálculo, os resultados (download, upload e ping) serão mostrados.
- No Windows, o prompt do DOS será minimizado automaticamente.
- Feche a janela clicando em "Fechar" ou pressionando a tecla Enter.
- Para depuração, abra o terminal minimizado e verifique os logs, que mostram detalhes como a localização do usuário e o servidor selecionado.

## Contribuindo
Sinta-se à vontade para abrir issues ou pull requests no GitHub para sugerir melhorias ou relatar problemas. Algumas ideias para contribuição:
- Adicionar suporte para salvar os resultados em um arquivo.
- Implementar suporte para outras APIs de teste de velocidade (ex.: M-Lab).
- Melhorar a interface gráfica com temas ou opções adicionais.

## Autor
**Miguel D'Alessandro Faria**  
- LinkedIn: [https://www.linkedin.com/in/miguel-faria-888171169/](https://www.linkedin.com/in/miguel-faria-888171169/)  
- GitHub: [https://github.com/miguelfaria009](https://github.com/miguelfaria009)

## Licença
Este projeto é de uso livre. Sinta-se à vontade para modificá-lo e distribuí-lo conforme suas necessidades.

## Notas
- **Geolocalização**: O script usa a API `ipinfo.io` para determinar sua localização com base no IP externo. Essa API tem um limite gratuito de 50.000 requisições por mês. Se você exceder esse limite, pode substituir por outra API, como `ip-api.com`.
- **Limitações**: O teste é realizado com servidores da Ookla (usados pelo `speedtest-cli`), que podem diferir dos servidores do M-Lab (usados pelo teste do Google). Isso pode causar discrepâncias nos resultados.
- **Condições Ideais**: Para melhores resultados, use uma conexão Ethernet, feche outros aplicativos que consumam banda e teste em horários de baixa demanda na rede.
