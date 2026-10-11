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

Não foram validados conformidade regulatória, autenticação, armazenamento, integrações ou desempenho com 6000 clientes.
