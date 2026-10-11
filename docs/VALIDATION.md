# Validação da primeira versão
Verificação TypeScript e compilação concluídas com sucesso.
Teste Playwright executado no ambiente de desenvolvimento:
- Buscar paciente e selecionar atendimento.
- Avançar check-in e iniciar atendimento.
- Guardar rascunho fictício.
- Simular recebimento sem pagamento externo.
- Rejeitar agendamento no mesmo horário do mesmo profissional.
- Criar novo agendamento.
- Tela de 390px sem transbordamento horizontal.
- Sem erros JavaScript no navegador durante esses fluxos.
Capturas desktop e mobile inspecionadas.

Reprodução: instalar Playwright em ambiente de teste, iniciar o aplicativo e executar tests/flows.cjs. BASE_URL e CHROMIUM_PATH são opcionais. A versão independente React/Vite foi compilada e os mesmos testes foram executados com sucesso. O arquivo tests/flows.cjs usa Playwright instalado em app/.

## Backend local
Instalação limpa em Ubuntu 24.04 com Docker no GitHub Actions:
https://github.com/jonathanfferreira/doctoragape/actions/runs/38110912727

- Compilação das versões Frappe/ERPNext/Marley fixadas no lock.
- Inicialização do site agape.localhost e bancos MariaDB/PostgreSQL.
- Inicialização Chatwoot v4.18.0 e resposta HTTP da sua interface.
- Resposta HTTP do Frappe.
- Criação de empresa, cliente, paciente, profissional, agendamento e atendimento fictícios.
- Criação de fatura em rascunho com total 90 BRL; sem cobrança externa.
- Reinício MariaDB/Frappe e comprovação de que os sete registros permanecem, com fatura ainda em rascunho no mesmo valor.

Reproduzir: `python3 infrastructure/local/start.py --restart-check`, com Docker disponível, ou o script Windows documentado em infrastructure/local/README.md. As credenciais são geradas localmente e os volumes não são removidos. No CI são efêmeros.

O script PowerShell foi preparado para Windows, mas não foi executado no computador do usuário. O CI roda os contêineres Linux e o mesmo procedimento Python.

Não foram validados conformidade regulatória, autenticação da interface própria, autorização por perfil, conexão entre interface e backend, isolamento entre clínicas, backup/restauração, WhatsApp, pagamentos, exportações dos fornecedores ou desempenho com 6000 clientes. O armazenamento validado acima restringe-se aos registros fictícios e ao reinício dos contêineres.
