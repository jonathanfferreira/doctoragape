# Ambiente local Doctor Ágape

Configuração preparada, ainda não executada com Docker nesta sessão. Não é implantação de produção. As tags de imagens-base podem mudar; os commits das aplicações Frappe são fixados no lock. PDFs com wkhtmltopdf e integrações externas não fazem parte desta etapa.

Requisitos: Docker Engine/Desktop com Compose v2, internet para builds e Python 3 para gerar arquivos locais de configuração. Reserve espaço para imagens e volumes; ajustar recursos após medir a instalação. O build compila as aplicações e pode demorar.

Execute a partir desta pasta:
1. python3 configure.py
2. docker compose config --quiet
3. docker compose build
4. docker compose up -d
5. docker compose logs -f init-frappe init-chatwoot

Frappe: http://agape.localhost:8000. Login Administrator e senha FRAPPE_ADMIN_PASSWORD no .env local. Se o navegador não resolver agape.localhost, testar localhost:8000: o site padrão foi definido com bench use.
Chatwoot: http://localhost:3000. Criar conta local de teste. Cadastro aberto é exclusivo desta configuração local.

Verificar módulos instalados:
docker compose exec frappe-web bench --site agape.localhost list-apps

Para pausar:
docker compose stop
Para parar e remover contêineres, preservando dados:
docker compose down

Não usar down -v para pausar: remove os volumes e dados.

## Limites
- Portas ligadas apenas a 127.0.0.1.
- Somente dados fictícios.
- A interface hospedada ainda não conversa com esses servidores locais.
- Chatwoot não está vinculado ao cadastro Frappe; próxima etapa é adaptador autenticado.
- Não configuramos WhatsApp, pagamentos, e-mail, produção, TLS ou prontuário regulatório.
- Initializers não reinstalam sites existentes; falhas parciais devem ser diagnosticadas pelos logs.
- Teste seguinte: criar paciente no Marley, consulta e atendimento, provar persistência; depois vincular faturamento e contatos Chatwoot.
- Credenciais .env e .chatwoot.env são ignoradas pelo Git. Não enviar em chat nem publicar.

## Referências
https://github.com/frappe/frappe_docker/blob/main/devcontainer-example/docker-compose.yml
https://github.com/earthians/marley/blob/version-15/.github/workflows/ci.yml
https://github.com/chatwoot/chatwoot/blob/v4.18.0/docker-compose.production.yaml
