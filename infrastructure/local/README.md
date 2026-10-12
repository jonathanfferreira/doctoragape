# Ambiente local Doctor Ágape

Instalação limpa verificada no GitHub Actions com Docker em Linux, incluindo um fluxo clínico fictício e persistência após reiniciar MariaDB/Frappe. O script PowerShell está preparado para Windows, mas não foi executado no computador do usuário. Não é implantação de produção. As tags de imagens-base podem mudar; os commits das aplicações Frappe são fixados no lock. PDFs com wkhtmltopdf e integrações externas não fazem parte desta etapa.

Requisitos: Docker Engine/Desktop com Compose v2, internet para builds e Python 3 para gerar arquivos locais de configuração. Reserve espaço para imagens e volumes; ajustar recursos após medir a instalação. O build compila as aplicações e pode demorar.

Execute a partir desta pasta:
1. python3 configure.py
2. docker compose config --quiet
3. docker compose build
4. docker compose up -d
5. docker compose logs -f init-frappe init-chatwoot

Frappe: http://agape.localhost:8000. Login Administrator e senha FRAPPE_ADMIN_PASSWORD no .env local. Se o navegador não resolver agape.localhost, testar localhost:8000: o site padrão foi definido com bench use.
Chatwoot: http://localhost:3000. Criar conta local de teste. Cadastro aberto é exclusivo desta configuração local: em produção, partir de `chatwoot.env.production.example` (cadastro fechado, TLS obrigatório) e nunca reutilizar o arquivo gerado para desenvolvimento.

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
- Próxima etapa: autenticar e conectar a interface ao cadastro/agenda/atendimento; vincular benefícios e contatos Chatwoot depois. O teste atual confirma criação de registros e fatura em rascunho, sem validar permissões de usuários ou contabilidade de produção.
- Credenciais .env e .chatwoot.env são ignoradas pelo Git. Não enviar em chat nem publicar.

## Referências
https://github.com/frappe/frappe_docker/blob/main/devcontainer-example/docker-compose.yml
https://github.com/earthians/marley/blob/version-15/.github/workflows/ci.yml
https://github.com/chatwoot/chatwoot/blob/v4.18.0/docker-compose.production.yaml

## Windows
Instalar Docker Desktop com backend WSL2 e Python 3. Esta sessão não instala programas no seu computador.
No PowerShell, clone o repositório e execute:

```powershell
git clone https://github.com/jonathanfferreira/doctoragape.git
cd doctoragape\infrastructure\local
powershell -ExecutionPolicy Bypass -File .\start-windows.ps1
```

Se o repositório já estiver clonado, execute apenas a última linha dentro de infrastructure/local. Git também precisa estar instalado para o clone.

O script verifica Docker, gera credenciais se não existirem, compila, inicializa e executa um fluxo fictício. Reinicia MariaDB/Frappe e confirma a permanência dos registros. Não sobrescreve senhas existentes, não limpa volumes e não envia mensagens nem pagamentos.
O teste cria empresa fictícia, paciente, profissional, consulta, evolução em rascunho e fatura em rascunho. É exclusivo do site agape.localhost, não aplica regras de prontuário ou contabilidade brasileira de produção.

Em Linux/macOS, executar python3 start.py --restart-check.
O workflow Backend installation and persistence testa o mesmo procedimento no GitHub Actions.

## Recuperação do Docker no Windows
O inicializador verifica o servidor Docker, tenta reiniciar o Docker Desktop quando ele não responde e aguarda até três minutos. O reinício pode interromper outros contêineres locais. Ele não redefine WSL, reinstala programas nem remove volumes.
Se houver DOCKER_API_VERSION definida, a execução ignora essa variável apenas nos subprocessos para permitir negociação automática, sem alterar a configuração do Windows.
Se o mecanismo continuar indisponível, salva docker-diagnostics.txt nesta pasta (ignorado pelo Git), com estado do WSL e versões/contexto Docker. Não coleta arquivos .env ou logs de aplicações. O diagnóstico não significa que a instalação foi concluída.

Atualizar uma cópia existente e tentar novamente no PowerShell, dentro desta pasta:
```powershell
git pull --ff-only
powershell -ExecutionPolicy Bypass -File .\start-windows.ps1
```
