/** Actualiza la matriz existente; conserva las hojas de inspección. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

async function cargarMotor() {
  try { return await import('@oai/artifact-tool'); }
  catch (original) {
    const modules = process.env.IHC_NODE_MODULES || process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
    if (modules) {
      const require = createRequire(path.join(path.resolve(modules), '..', 'package.json'));
      return await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
    }
    throw new Error('La matriz requiere un entorno Node.js con @oai/artifact-tool disponible. Consulta scripts/README.md.', {cause: original});
  }
}

const {FileBlob, SpreadsheetFile} = await cargarMotor();
const argv = process.argv.slice(2);
if (argv.length === 1 && argv[0] === '--comprobar') {
  console.log('Motor de matriz disponible.');
  process.exit(0);
}
const allowed = new Set(['--datos', '--matriz', '--qa-dir']);
const options = {};
for (let i = 0; i < argv.length; i += 2) {
  if (!allowed.has(argv[i]) || !argv[i + 1]) throw new Error('Uso: generar_matriz.mjs --datos datos.json --matriz matriz_ux.xlsx [--qa-dir carpeta]');
  options[argv[i].slice(2)] = argv[i + 1];
}
if (!options.datos || !options.matriz) throw new Error('Se requieren --datos y --matriz. Usa generar_curva_y_matriz.py para el flujo completo.');
const d = JSON.parse(await fs.readFile(options.datos, 'utf8'));
const participants = ['P1', 'P2', 'P3'];
const versions = ['A_original', 'B_rediseno'];
const moments = ['M1', 'M2', 'M3', 'M4', 'M5'];
const fields = ['participante', 'version', 'momento', 'valor', 'emocion_evaluacion', 'nota_evaluacion', 'captura_referencia', 'tipo_registro'];
if (d.schema_version !== 1 || d.records?.length !== 30 || d.moments?.length !== 5) throw new Error('El JSON no corresponde al esquema validado de la evaluación.');
const unique = new Set();
for (const r of d.records) {
  const key = [r.participante, r.version, r.momento].join('/');
  if (unique.has(key) || !participants.includes(r.participante) || !versions.includes(r.version) || !moments.includes(r.momento)
      || !Number.isInteger(r.valor) || r.valor < -3 || r.valor > 3 || r.tipo_registro !== 'evaluacion_ux'
      || fields.some(f => r[f] === null || r[f] === undefined || String(r[f]).trim() === '')) throw new Error(`Registro inválido o duplicado: ${key}`);
  unique.add(key);
}
const w = await SpreadsheetFile.importXlsx(await FileBlob.load(options.matriz));
const m = w.worksheets.getItem('Matriz UX');
let s;
try { s = w.worksheets.getItem('Datos de evaluación'); }
catch { s = w.worksheets.add('Datos de evaluación'); }
const navy = '#203C87';
const body = {name: 'Arial', size: 11, color: '#111827'};
function header(sheet, range) {
  sheet.getRange(range).format = {fill: navy, font: {...body, bold: true, color: '#FFFFFF'}, wrapText: true,
    horizontalAlignment: 'center', verticalAlignment: 'center', rowHeight: 40};
}
s.showGridLines = false;
s.getRange('A1:I51').format.font = body;
s.getRange('A1:I51').format.verticalAlignment = 'center';
s.getRange('A1:I1').merge();
s.getRange('A1').values = [['Datos y cálculos de la evaluación emocional']];
s.getRange('A1:I1').format.font = {...body, size: 15, bold: true};
s.getRange('A1:I1').format.rowHeight = 30;
s.getRange('A2:I2').merge();
s.getRange('A2').values = [[`Fuente: ${d.source.path}. Escala de −3 a +3; cero indica neutralidad.`]];
s.getRange('A2:I2').format = {font: {...body, italic: true}, wrapText: true, rowHeight: 30};
s.getRange('A4:I4').values = [[...fields, 'validacion']];
header(s, 'A4:I4');
s.getRange('A5:H34').values = d.records.map(r => fields.map(f => r[f]));
s.getRange('A5:H34').format.wrapText = true;
s.getRange('A5:I34').format.rowHeight = 34;
s.getRange('D5:D34').setNumberFormat('0');
s.getRange('D5:D34').format.fill = '#FFF4CC';
s.getRange('D5:D34').dataValidation = {rule: {type: 'whole', operator: 'between', formula1: -3, formula2: 3}};
for (const [col, values] of [['A', participants], ['B', versions], ['C', moments]]) {
  s.getRange(`${col}5:${col}34`).dataValidation = {rule: {type: 'list', values}};
}
for (let r = 5; r <= 34; r++) {
  const f = `=IFERROR(IF(AND(ISNUMBER(D${r}),D${r}>=-3,D${r}<=3,D${r}=INT(D${r}),LEN(TRIM(E${r}))>0,LEN(TRIM(F${r}))>0,LEN(TRIM(G${r}))>0,OR(A${r}="P1",A${r}="P2",A${r}="P3"),OR(B${r}="A_original",B${r}="B_rediseno"),OR(C${r}="M1",C${r}="M2",C${r}="M3",C${r}="M4",C${r}="M5"),H${r}="evaluacion_ux",COUNTIFS($A$5:$A$34,A${r},$B$5:$B$34,B${r},$C$5:$C$34,C${r})=1),"Válido","Revisar"),"Revisar")`;
  s.getRange(`I${r}`).formulas = [[f]];
}
s.getRange('I5:I34').conditionalFormats.deleteAll();
s.getRange('I5:I34').conditionalFormats.add('containsText', {text: 'Revisar', format: {fill: '#FEE2E2', font: {color: '#991B1B', bold: true}}});
s.getRange('H36:I36').values = [['Control de entradas', 'Registros válidos']];
s.getRange('H37').values = [['Se requieren 30 registros únicos y completos.']];
s.getRange('I37').formulas = [['=COUNTIF(I5:I34,"Válido")']];
s.getRange('I37').setNumberFormat('0');
s.getRange('H36:I37').format.wrapText = true;
s.getRange('H36:I37').format.rowHeight = 30;
s.getRange('A36:F36').merge();
s.getRange('A36').values = [['Resumen por momento']];
s.getRange('A36:F36').format.font = {...body, bold: true};
s.getRange('A38:F38').values = [['Momento', 'Media A', 'Media B', 'Diferencia B menos A', 'Registros A', 'Registros B']];
header(s, 'A38:F38');
for (let i = 0; i < moments.length; i++) {
  const r = i + 39;
  s.getRange(`A${r}`).values = [[moments[i]]];
  s.getRange(`B${r}:F${r}`).formulas = [[
    `=IF($I$37<>30,NA(),AVERAGEIFS($D$5:$D$34,$B$5:$B$34,"A_original",$C$5:$C$34,A${r}))`,
    `=IF($I$37<>30,NA(),AVERAGEIFS($D$5:$D$34,$B$5:$B$34,"B_rediseno",$C$5:$C$34,A${r}))`,
    `=C${r}-B${r}`,
    `=COUNTIFS($B$5:$B$34,"A_original",$C$5:$C$34,A${r})`,
    `=COUNTIFS($B$5:$B$34,"B_rediseno",$C$5:$C$34,A${r})`,
  ]];
}
s.getRange('A44').values = [['Media global']];
s.getRange('B44:F44').formulas = [[
  '=IF($I$37<>30,NA(),AVERAGEIF($B$5:$B$34,"A_original",$D$5:$D$34))',
  '=IF($I$37<>30,NA(),AVERAGEIF($B$5:$B$34,"B_rediseno",$D$5:$D$34))',
  '=C44-B44', '=COUNTIF($B$5:$B$34,"A_original")', '=COUNTIF($B$5:$B$34,"B_rediseno")',
]];
s.getRange('A46:F46').merge();
s.getRange('A46').values = [['Resumen por código de participante']];
s.getRange('A46:F46').format.font = {...body, bold: true};
s.getRange('A48:D48').values = [['Participante', 'Media A', 'Media B', 'Diferencia B menos A']];
header(s, 'A48:D48');
for (let i = 0; i < participants.length; i++) {
  const r = i + 49;
  s.getRange(`A${r}`).values = [[participants[i]]];
  s.getRange(`B${r}:D${r}`).formulas = [[
    `=IF($I$37<>30,NA(),AVERAGEIFS($D$5:$D$34,$B$5:$B$34,"A_original",$A$5:$A$34,A${r}))`,
    `=IF($I$37<>30,NA(),AVERAGEIFS($D$5:$D$34,$B$5:$B$34,"B_rediseno",$A$5:$A$34,A${r}))`,
    `=C${r}-B${r}`,
  ]];
}
s.getRange('B39:D44').setNumberFormat('0.00');
s.getRange('B49:D51').setNumberFormat('0.00');
s.getRange('E39:F44').setNumberFormat('0');
s.getRange('A39:F44').format.rowHeight = 26;
s.getRange('A49:D51').format.rowHeight = 26;
s.getRange('A44:F44').format = {fill: '#E9EEF7', font: {...body, bold: true}};
for (const [col, width] of [['A',18],['B',18],['C',19],['D',23],['E',23],['F',74],['G',22],['H',24],['I',18]]) {
  s.getRange(`${col}1:${col}51`).format.columnWidth = width;
}
s.freezePanes.freezeRows(4);
s.freezePanes.freezeColumns(1);
// Extender la matriz y sus estilos; las otras dos hojas conservan sus valores.
m.getRange('K4:L10').copyFrom(m.getRange('I4:J10'), 'all');
m.getRange('K4:L4').values = [['Resultado en B', 'Diferencia B menos A']];
m.getRange('K1:K10').format.columnWidth = 37;
m.getRange('L1:L10').format.columnWidth = 18;
m.getRange('A1:L1').merge();
m.getRange('A2:L2').merge();
m.getRange('A2').values = [['Emociones anotadas y medias de los 30 registros publicados. Escala de −3 a +3. Los resultados describen la versión evaluada; las correcciones posteriores se documentan en rediseño/correcciones_pendientes.md.']];
m.getRange('A2:L2').format = {wrapText: true, rowHeight: 32, font: {name:'Arial',size:11,color:'#374151',italic:true}};
m.getRange('D4').values = [['Emociones anotadas en A']];
m.getRange('E4').values = [['Media A original']];
m.getRange('I4').values = [['Emociones anotadas en B']];
m.getRange('J4').values = [['Media B rediseño']];
m.getRange('D10').values = [['Media global']];
const dataRef = "'Datos de evaluación'!";
for (let i = 0; i < moments.length; i++) {
  const r = i + 5, calc = i + 39;
  for (const [col, version] of [['D','A_original'],['I','B_rediseno']]) {
    const emotions = [...new Set(d.records.filter(x => x.version === version && x.momento === moments[i]).map(x => x.emocion_evaluacion))];
    m.getRange(`${col}${r}`).values = [[emotions.join(' / ')]];
  }
  m.getRange(`E${r}`).formulas = [[`=${dataRef}B${calc}`]];
  m.getRange(`J${r}`).formulas = [[`=${dataRef}C${calc}`]];
  m.getRange(`L${r}`).formulas = [[`=${dataRef}D${calc}`]];
  m.getRange(`K${r}`).formulas = [[`=IF(${dataRef}$I$37<>30,"Revisar registros",IF(COUNTIFS(${dataRef}$B$5:$B$34,"B_rediseno",${dataRef}$C$5:$C$34,"${moments[i]}",${dataRef}$D$5:$D$34,"<0")>0,"B conserva valoraciones negativas",IF(J${r}=0,"Media neutra en B","B sin valoraciones negativas")))`]];
}
for (const [col, source] of [['E','B'],['J','C'],['L','D']]) {
  m.getRange(`${col}10`).formulas = [[`=${dataRef}${source}44`]];
  m.getRange(`${col}5:${col}10`).setNumberFormat('0.00');
}
m.getRange('K10').clear({applyTo:'contents'});
w.recalculate();
function near(actual, expected, label) {
  if (typeof actual !== 'number' || Math.abs(actual - expected) > 1e-9) throw new Error(`${label}: ${actual} != ${expected}`);
}
for (let i = 0; i < moments.length; i++) {
  for (const [col, key] of [['E','media_A'], ['J','media_B'], ['L','diferencia_B_menos_A']]) {
    near(m.getRange(`${col}${i+5}`).values[0][0], d.summary[i][key], `${moments[i]} ${key}`);
  }
}
for (const [col, key] of [['E','media_A'],['J','media_B'],['L','diferencia_B_menos_A']]) near(m.getRange(`${col}10`).values[0][0], d.global[key], key);
if (s.getRange('I37').values[0][0] !== 30) throw new Error('No hay 30 registros válidos en la hoja de datos.');
if (options['qa-dir']) {
  const qa = path.resolve(options['qa-dir']);
  await fs.mkdir(qa, {recursive:true});
  // Comprobar cero, vacío y duplicación. Restaurar todas las entradas antes de exportar.
  const original = s.getRange('D5').values[0][0];
  const baseline = m.getRange('E5').values[0][0];
  s.getRange('D5').values = [[original + 1]];
  w.recalculate();
  near(m.getRange('E5').values[0][0], baseline + 1/3, 'Recalcular al cambiar un valor');
  s.getRange('D5').values = [[null]];
  w.recalculate();
  if (s.getRange('I5').values[0][0] !== 'Revisar' || typeof m.getRange('E5').values[0][0] === 'number') throw new Error('Una entrada vacía se interpretó como válida.');
  s.getRange('D5').values = [[original]];
  const originalID = s.getRange('A5').values[0][0];
  s.getRange('A5').values = [['P2']];
  w.recalculate();
  if (s.getRange('I5').values[0][0] !== 'Revisar' || typeof m.getRange('E5').values[0][0] === 'number') throw new Error('Una clave duplicada se interpretó como válida.');
  s.getRange('A5').values = [[originalID]];
  w.recalculate();
  near(m.getRange('E5').values[0][0], baseline, 'Restaurar las entradas');
  const scan = await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1500});
  await fs.writeFile(path.join(qa,'formulas.json'), scan.ndjson);
  for (const [sheetName, range, name] of [
    ['Matriz UX','A1:F10','matriz_izquierda'],['Matriz UX','G4:L10','matriz_derecha'],
    ['Matriz UX','A1:L2','matriz_titulo'],['Datos de evaluación','A1:I2','datos_titulo'],['Datos de evaluación','A4:D14','datos_valores'],['Datos de evaluación','E4:I12','datos_notas'],
    ['Datos de evaluación','A36:F51','datos_resumen'],['Verificación','A1:D16','verificacion'],
    ['Verificación','A19:F27','contrastes'],['Heurísticas','A1:C9','heuristicas'],
  ]) {
    const b = await w.render({sheetName, range, scale:1, format:'png'});
    await fs.writeFile(path.join(qa,`${name}.png`),new Uint8Array(await b.arrayBuffer()));
  }
}
await (await SpreadsheetFile.exportXlsx(w)).save(options.matriz);
console.log('Matriz actualizada: 30 registros, medias por momento, medias globales y diferencias enlazadas.');
