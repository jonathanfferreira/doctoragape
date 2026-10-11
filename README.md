# Doctor Ágape

Plataforma unificada de clínica em desenvolvimento. Esta entrega é um protótipo com dados fictícios, não um prontuário de produção.

## Interface local
Requisitos: Node 22 e npm.
Dentro de app/:
1. npm ci
2. npm run dev
Abrir http://localhost:5173.
Verificação: npm run typecheck e npm run build.
Teste de fluxos: instalar Chromium com npx playwright install chromium, iniciar a interface e executar npm run test:flows.

Recepção, agenda, consulta de paciente, elegibilidade ilustrativa, evolução fictícia e recebimentos simulados. Dados em memória; recarregar descarta alterações. Sem login, assinatura, dados reais ou integração externa.

## Backend
Seguir infrastructure/local/README.md para o ambiente Docker de ERPNext/Marley e Chatwoot. Os arquivos foram preparados e analisados; instalação Docker ainda não executada.
Fontes e commits candidatos em infrastructure/open-source/sources.lock.json.
Arquitetura em docs/ARCHITECTURE.md.

## Origem e licenças
A interface customizada foi transferida do protótipo hospedado, preservando seu comportamento. Esta versão usa React/Vite e não depende dos SDKs internos da hospedagem. A demonstração hospedada continua separada; commits aqui não a atualizam automaticamente.
Logotipo da Doctor Ágape obtido do site oficial para este projeto. Não concedemos licença de terceiros ou da marca.
ERPNext/Marley são GPLv3; Chatwoot tem MIT fora de enterprise. Ver avisos upstream antes de incorporar/distribuir. O projeto próprio ainda não definiu uma licença de distribuição.

## Estado
Primeira fase: validar UX com a equipe e executar instalação limpa, persistência, isolamento e restauração do backend local. A interface ainda não se conecta aos servidores Docker.
