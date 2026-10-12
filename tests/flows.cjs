const {chromium}=require('../app/node_modules/playwright');
(async()=>{
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH ? {executablePath:process.env.CHROMIUM_PATH} : {}),args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto(process.env.BASE_URL || 'http://localhost:5173/');await page.getByLabel('E-mail de demonstração').fill('admin@demo.local');await page.getByLabel('Senha',{exact:true}).fill('demo');await page.getByRole('button',{name:'Entrar',exact:true}).click();await page.getByRole('heading',{name:'Tudo pronto para atender.'}).waitFor();
await page.waitForTimeout(1500);await page.getByLabel('Buscar paciente',{exact:true}).fill('Beatriz');await page.waitForFunction(()=>document.querySelectorAll('.appointment').length===1);
await page.locator('.appointment').click();await page.getByRole('button',{name:'Fazer check-in',exact:true}).click();await page.getByRole('button',{name:'Iniciar atendimento',exact:true}).click();await page.getByRole('button',{name:'Abrir evolução'}).click();
await page.getByLabel('Evolução do atendimento').fill('Anotação fictícia para testar o rascunho.');await page.getByRole('button',{name:'Guardar rascunho'}).click();await page.locator('.draft').waitFor();
await page.getByRole('button',{name:'Financeiro',exact:true}).click();await page.getByRole('button',{name:'Simular recebimento'}).first().click();
await page.getByRole('button',{name:'+ Agendar consulta'}).click();await page.getByLabel('Horário',{exact:true}).fill('09:30');await page.getByRole('button',{name:'Confirmar agendamento'}).click();await page.getByRole('alert').waitFor();await page.getByLabel('Horário',{exact:true}).fill('11:00');await page.getByRole('button',{name:'Confirmar agendamento'}).click();
await page.getByRole('button',{name:'Recepção',exact:true}).click();await page.waitForFunction(()=>document.querySelectorAll('.appointment').length===6);
await page.screenshot({path:process.env.DESKTOP_SCREENSHOT || '/tmp/agape-desktop.png'});
await page.setViewportSize({width:390,height:844});if(await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth))throw Error('mobile overflow');
await page.screenshot({path:process.env.MOBILE_SCREENSHOT || '/tmp/agape-mobile.png'});
if(errors.length)throw Error(errors.join('\n'));
console.log('PASS: search, check-in, start, draft, simulated payment, booking conflict, booking creation, mobile overflow, browser errors.');
await browser.close();
})();
