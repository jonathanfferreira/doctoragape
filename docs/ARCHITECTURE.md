# Doctor Ágape: arquitetura inicial

Status: protótipo de UX React/Vite, exclusivamente fictício e em memória. Login simulado com perfis fictícios restringe os módulos por perfil (recepção, clínico, financeiro e administrador); ainda não há autenticação real nem persistência, assinatura, cobrança ou conexão externa. Não utilizar em atendimento real.

## Componentes candidatos
Frappe/ERPNext para gestão, Marley/Frappe Health para clínica, Chatwoot para comunicação, módulo próprio de benefícios e avaliação específica SST/eSocial. A base Docker separada instala ERPNext/Marley e Chatwoot, com versões documentadas no lock. O protótipo de interface ainda não está conectado a ela.

Versões e licenças verificadas nos commits registrados: Frappe MIT, ERPNext/Marley GPLv3 e Chatwoot MIT fora da área enterprise. Reavaliar compatibilidade e obrigações de distribuição ao atualizar ou incorporar código.

## Produção
Recomenda-se avaliar um site/banco Frappe por clínica. Isolar usuários, anexos, backups, chaves e integrações. Backend próprio coordena adaptadores e identidade comum do paciente. API é a integração padrão, MCP é uma camada opcional posterior.

Prontuário exige autorização por perfil e vínculo com atendimento, auditoria de acesso e mudanças, autoria, rascunho separado de documento finalizado, retificações sem sobrescrever original. Validar LGPD, guarda e assinatura com especialistas antes de operação real.

Migração por APIs/exportações autorizadas: preservar identificadores de origem, datas, autoria, anexos e vínculos. Importação idempotente, conciliação de contagens, amostragem, origem disponível durante transição e restauração testada.

Mensagens do Chatwoot não são convertidas automaticamente em prontuário. Minimizar dados clínicos nos canais de comunicação.

## Próxima fase
Conectar a interface ao backend por APIs autenticadas, definir perfis e testar autorização. A instalação automatizada já verifica empresa/cliente/paciente/profissional/agendamento/atendimento/fatura em rascunho e permanência após reiniciar o banco. Validar os fluxos com a equipe, testar backups e isolamento antes de integrar fornecedores e preparar piloto clínico.
