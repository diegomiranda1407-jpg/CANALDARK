# O Mundo das Pequenas Aventuras

Gerador inicial de episódios infantis em português brasileiro para o canal.

## O que esta primeira versão faz
- Cria ilustrações originais simples em estilo 2D/2.5D com Python/Pillow.
- Gera narração em português usando eSpeak NG (voz sintética gratuita).
- Monta um vídeo MP4 com movimentos suaves de câmera usando FFmpeg.
- Publica o MP4 como artefato da execução do GitHub Actions.

## Executar
No GitHub, abra **Actions** e execute **Gerar episódio** em **Run workflow**. Também há execução automática semanal.

## Limitações honestas
Esta versão é um protótipo funcional de animação 2D com ilustrações vetoriais/rasterizadas e voz sintética. Não usa um serviço de vídeo generativo nem produz animação 3D. A qualidade da voz depende da voz pt-br disponível no eSpeak NG. A execução gera um arquivo para revisão; não envia automaticamente ao YouTube.

## Próxima etapa
A publicação no YouTube exige autorização OAuth da conta do canal e configuração segura dos segredos do repositório. Isso não deve ser improvisado nem expor senhas.
