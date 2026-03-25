# Baixador de Recursos (Audio & Video)

Este é um projeto simples e eficiente desenvolvido em Python para baixar vídeos e áudios de diversas plataformas da web (como YouTube e outras suportadas pelo `yt-dlp`). Ele oferece uma interface gráfica (GUI) amigável para facilitar o processo, permitindo escolher entre diferentes formatos e qualidades.

## 🚀 Funcionalidades

- **Três Modos de Download:**
  - **Tudo (Vídeo + Áudio):** Baixa o vídeo completo em formato MP4.
  - **Só Áudio (MP3):** Extrai apenas o áudio e converte para MP3 (128, 192 ou 320 kbps).
  - **Vídeo sem Áudio:** Baixa apenas a trilha de vídeo em MP4.
- **Interface Gráfica Moderna:** Desenvolvida com Tkinter, oferecendo uma experiência visual limpa e intuitiva.
- **Gerenciamento de Pasta:** Permite definir e abrir facilmente a pasta de destino dos arquivos.
- **Processamento em Segundo Plano:** Os downloads não travam a interface, permitindo acompanhar o progresso em tempo real.

## 🛠️ Requisitos

Para rodar este projeto, você precisará de:

1.  **Python 3.12 ou superior**
2.  **[uv](https://github.com/astral-sh/uv):** Um instalador e gerenciador de pacotes Python extremamente rápido.
3.  **FFmpeg:** Essencial para que o `yt-dlp` consiga converter áudios e unir trilhas de vídeo e áudio.
    - *No Windows:* Você pode baixar o binário em [ffmpeg.org](https://ffmpeg.org/download.html) ou via `choco install ffmpeg` / `scoop install ffmpeg`. Certifique-se de que ele esteja no seu `PATH`.

## 📦 Como Usar com UV

O `uv` facilita muito a execução do projeto sem que você precise se preocupar em criar ambientes virtuais manualmente.

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/downloader-audios-efects.git
cd downloader-audios-efects
```

### 2. Executar o Projeto
Com o `uv` instalado, basta rodar o comando abaixo na raiz do projeto. O `uv` criará o ambiente virtual e instalará as dependências automaticamente na primeira execução:

```bash
uv run main.py
```

### 3. Usando o Atalho (Windows)
Se você estiver no Windows, pode simplesmente dar um clique duplo no arquivo `downloader.bat`. Ele executará o comando `uv run main.py` para você.

## 📂 Estrutura do Projeto

- `main.py`: Código principal da aplicação (Interface e lógica de download).
- `pyproject.toml`: Configurações do projeto e dependências (gerenciado pelo `uv`).
- `downloader.bat`: Script de inicialização rápida para Windows.
- `uv.lock`: Arquivo de trava de versões das dependências.

## ⚠️ Observação Importante
Certifique-se de que o **FFmpeg** está instalado e acessível pelo terminal. Sem ele, a conversão para MP3 e a união de vídeo/áudio de alta qualidade falharão.

---
Desenvolvido para facilitar a captura de efeitos sonoros e recursos audiovisuais.
