# Baixador de Recursos (Audio & Video)

Este é um projeto simples e eficiente desenvolvido em Python para baixar vídeos e áudios de diversas plataformas da web (como YouTube e outras suportadas pelo `yt-dlp`). Ele oferece uma interface gráfica (GUI) amigável para facilitar o processo, permitindo escolher entre diferentes formatos e qualidades.

## 🚀 Funcionalidades

- **Múltiplos Modos de Download:**
  - **Tudo (Vídeo + Áudio):** Baixa o vídeo completo, com opções em MP4 (padrão), WebM (Alta Qualidade) e MKV.
  - **Só Áudio:** Extrai o áudio e converte para MP3 (128, 192 ou 320 kbps), WAV (Qualidade Lossless/Sem perdas) ou FLAC (Lossless comprimido).
  - **Vídeo sem Áudio:** Baixa apenas a trilha de vídeo em MP4 (excelente para edições e b-rolls).
- **Interface Gráfica Moderna:** Desenvolvida com Tkinter, oferecendo uma experiência visual limpa e intuitiva.
- **Verificação de Sistema:** Checa automaticamente se o FFmpeg está instalado ao abrir o aplicativo, alertando o usuário para evitar erros de conversão.
- **Gerenciamento de Pasta:** Permite definir e abrir facilmente a pasta de destino dos arquivos nativamente pelo sistema.
- **Processamento em Segundo Plano:** Os downloads (usando threads) não travam a interface, permitindo acompanhar o progresso em tempo real e adicionar novas URLs.

## 🛠️ Requisitos

Para rodar este projeto, você precisará de:

1.  **Python 3.12 ou superior**
2.  **[uv](https://github.com/astral-sh/uv):** Um instalador e gerenciador de pacotes Python extremamente rápido.
3.  **FFmpeg:** Essencial para que o `yt-dlp` consiga converter áudios e unir trilhas de vídeo e áudio.
    - *No Windows:* Você pode baixar o binário em [ffmpeg.org](https://ffmpeg.org/download.html) ou via `choco install ffmpeg` / `scoop install ffmpeg`. Certifique-se de que ele esteja no seu `PATH`.

## 📦 Instalação e Execução (com UV)

O `uv` facilita muito a execução e o build do projeto. Escolha o comando de acordo com o seu perfil:

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/downloader-audios-efects.git
cd downloader-audios-efects
```

### 2. Escolha o seu Perfil

#### 👤 Para Usuários (Apenas rodar o app)
Para uma instalação limpa, contendo apenas o essencial para baixar os arquivos:
```bash
uv sync --no-dev
uv run poe start
```

#### 🛠️ Para Desenvolvedores (Build e Release)
Se você deseja modificar o código ou gerar o executável (`.exe`) para Windows:
```bash
# Instala todas as dependências (App + Dev Tools)
uv sync

# Comando para gerar o executável em uma pasta /dist
uv run poe build
```

### 3. Usando o Atalho (Windows)
Se você estiver no Windows, pode simplesmente dar um clique duplo no arquivo `downloader.bat`. Ele executará o comando `uv run poe start` para você.

## 📂 Estrutura do Projeto

- `main.py`: Código principal da aplicação (Interface e lógica de download).
- `pyproject.toml`: Configurações do projeto e dependências (gerenciado pelo `uv`).
- `downloader.bat`: Script de inicialização rápida para Windows.
- `uv.lock`: Arquivo de trava de versões das dependências.

## ⚠️ Observação Importante
Certifique-se de que o **FFmpeg** está instalado e acessível pelo terminal. Sem ele, a conversão para MP3 e a união de vídeo/áudio de alta qualidade falharão.

---
Desenvolvido para facilitar a captura de efeitos sonoros e recursos audiovisuais.
