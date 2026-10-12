export type Role='recepcao'|'clinico'|'financeiro'|'admin';
export type Module='Recepção'|'Pacientes'|'Atendimento'|'Benefícios'|'Financeiro'|'Integrações';
export interface Session{name:string;role:Role;}
export interface AuthService{
  login(email:string,password:string):Session|null;
  logout():void;
  modulesFor(role:Role):Module[];
}
export const MODULES:Module[]=['Recepção','Pacientes','Atendimento','Benefícios','Financeiro','Integrações'];
const ROLE_MODULES:Record<Role,Module[]>={
  recepcao:['Recepção','Pacientes','Benefícios'],
  clinico:['Recepção','Pacientes','Atendimento','Benefícios'],
  financeiro:['Recepção','Financeiro'],
  admin:MODULES,
};
export const ROLE_LABEL:Record<Role,string>={
  recepcao:'Recepção',clinico:'Clínico',financeiro:'Financeiro',admin:'Administrador',
};
const DEMO_PASSWORD='demo';
const users:Record<string,Session>={
  'recepcao@demo.local':{name:'Recepção Demo',role:'recepcao'},
  'clinico@demo.local':{name:'Clínico Demo',role:'clinico'},
  'financeiro@demo.local':{name:'Financeiro Demo',role:'financeiro'},
  'admin@demo.local':{name:'Administrador Demo',role:'admin'},
};
export const DEMO_ACCOUNTS=Object.keys(users);
// Mock em memória apenas para o protótipo. Na produção, esta interface será
// implementada pelo cliente de API do Frappe (login/sessão), com autorização
// e filtragem de registros no servidor — nunca confiando no frontend.
const service:AuthService={
  login(email,password){
    const normalized=email.trim().toLowerCase();
    const session=users[normalized];
    return password===DEMO_PASSWORD&&session?{...session}:null;
  },
  logout(){},
  modulesFor(role){return ROLE_MODULES[role];},
};
export const auth:AuthService=service;
