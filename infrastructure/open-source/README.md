# Base open source da Doctor Ágape

Seleção inicial pesquisada em 11/10/2026. A compatibilidade conjunta ainda exige execução.

| Componente | Versão candidata | Uso |
| --- | --- | --- |
| Frappe | 15.122.0 | Framework, autenticação, permissões e API |
| ERPNext | 15.122.0 | Cadastros e financeiro |
| Marley (app healthcare) | 15.2.4 | Pacientes, consultas, registros e laboratório |
| Chatwoot | 4.18.0 | Comunicação, serviço separado |

sources.lock.json fixa commits exatos. O script scripts/fetch-upstream.py DESTINO baixa esses commits para análise em diretório novo; não instala ou executa código upstream.

## Compatibilidade
ERPNext version-15 exige Frappe >=15.111.0 e <16.0.0; 15.122.0 satisfaz essa faixa.
Marley version-15 declara ERPNext obrigatório em healthcare/hooks.py. Seu CI usa o mesmo branch para Frappe e ERPNext, Python 3.10, Node 20 e MariaDB 10.6. Isso sustenta a escolha da família 15 para a prova de conceito, mas não comprova que os commits passaram juntos.
Branches develop de ERPNext e Marley dependem de Frappe 17 de desenvolvimento.
Chatwoot é Rails/Sidekiq com PostgreSQL/pgvector, Redis e armazenamento próprio.

## Implantação
ERPNext e Marley compartilham o site Frappe; criar módulo Doctor Ágape de extensões. Chatwoot mantém serviço e banco separados. Interface acessa backend autenticado; este usa APIs e vínculos de identificadores. Credenciais não vão para o navegador.

O Worker JavaScript do protótipo não executa diretamente Frappe/Python ou Chatwoot/Rails. Ambiente dedicado ou hospedagem gerenciada é necessário. Nenhuma contratação realizada.

## Licenças
ERPNext e Marley: GPLv3, uso comercial permitido cumprindo obrigações aplicáveis, especialmente na distribuição de alterações. Não assumir que código derivado pode ser fechado.
Chatwoot fora de enterprise: MIT, preservando avisos; enterprise tem licença separada. API não elimina automaticamente obrigações de licença.
Preservar licenças upstream. Frappe MIT deve ser conferido no commit fixado na instalação.

## Critérios de conclusão
Instalar módulos sem falha; criar paciente e consulta fictícios; ligar faturamento; integrar contato e conversa Chatwoot por API sem mensagens reais; provar persistência na interface; testar isolamento entre clínicas e restauração de backup antes de dados reais.

## Fontes oficiais
- https://github.com/frappe/erpnext/blob/version-15/pyproject.toml
- https://github.com/earthians/marley/blob/version-15/healthcare/hooks.py
- https://github.com/earthians/marley/blob/version-15/.github/workflows/ci.yml
- https://github.com/earthians/marley/blob/develop/license.txt
- https://github.com/chatwoot/chatwoot/blob/v4.18.0/docker-compose.production.yaml
- https://github.com/chatwoot/chatwoot/blob/develop/LICENSE
