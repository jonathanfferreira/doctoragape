# Doctor Ágape: arquitetura inicial

Status: protótipo de UX React/Vite, exclusivamente fictício e em memória. Sem login, persistência, assinatura, cobrança ou conexão externa. Não utilizar em atendimento real.

## Componentes candidatos
Frappe/ERPNext para gestão, Marley/Frappe Health para clínica, Chatwoot para comunicação, módulo próprio de benefícios e avaliação específica SST/eSocial. Nenhum desses componentes está instalado neste protótipo.

Validar versões, manutenção e licenças nos repositórios antes de incorporar código. ERPNext GPLv3 e Frappe MIT precisam de confirmação na versão adotada; verificar licença do Marley e separar Chatwoot comunitário/empresarial.

## Produção
Recomenda-se avaliar um site/banco Frappe por clínica. Isolar usuários, anexos, backups, chaves e integrações. Backend próprio coordena adaptadores e identidade comum do paciente. API é a integração padrão, MCP é uma camada opcional posterior.

Prontuário exige autorização por perfil e vínculo com atendimento, auditoria de acesso e mudanças, autoria, rascunho separado de documento finalizado, retificações sem sobrescrever original. Validar LGPD, guarda e assinatura com especialistas antes de operação real.

Migração por APIs/exportações autorizadas: preservar identificadores de origem, datas, autoria, anexos e vínculos. Importação idempotente, conciliação de contagens, amostragem, origem disponível durante transição e restauração testada.

Mensagens do Chatwoot não são convertidas automaticamente em prontuário. Minimizar dados clínicos nos canais de comunicação.

## Próxima fase
Validar fluxo com equipe, instalar versões compatíveis de ERPNext/Marley em ambiente dedicado e provar cadastro-agendamento-atendimento-financeiro com dados fictícios. Só depois integrar fornecedores e preparar piloto com autenticação e armazenamento adequado.
