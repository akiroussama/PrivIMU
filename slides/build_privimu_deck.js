const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'PrivIMU Team';
pptx.subject = 'IoT Security project - IMU motion privacy';
pptx.title = 'PrivIMU - Motion Anonymity Attack';
pptx.company = 'SUP\'COM';
pptx.lang = 'fr-FR';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'fr-FR',
};
pptx.defineLayout({ name: 'LAYOUT_WIDE', width: 13.333, height: 7.5 });

const C = {
  bg: '0B1020',
  bg2: '111827',
  panel: '172033',
  panel2: '1E293B',
  text: 'F8FAFC',
  muted: '94A3B8',
  line: '334155',
  cyan: '22D3EE',
  blue: '38BDF8',
  green: '34D399',
  amber: 'FBBF24',
  red: 'FB7185',
  violet: 'A78BFA',
  white: 'FFFFFF',
};

const W = 13.333;
const H = 7.5;

function addBg(slide) {
  slide.background = { color: C.bg };
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.bg }, line: { color: C.bg } });
  slide.addShape(pptx.ShapeType.arc, { x: -1.7, y: -1.5, w: 4.6, h: 4.6, line: { color: C.cyan, transparency: 78, width: 1.5 }, adjustPoint: 0.22 });
  slide.addShape(pptx.ShapeType.arc, { x: 10.2, y: 5.2, w: 4.0, h: 4.0, line: { color: C.violet, transparency: 80, width: 1.3 }, adjustPoint: 0.22 });
}

function addFooter(slide, idx) {
  slide.addText('PrivIMU - IoT Security / Motion Privacy', { x: 0.55, y: 7.12, w: 6.5, h: 0.22, fontFace: 'Aptos', fontSize: 7.5, color: C.muted, margin: 0 });
  slide.addText(String(idx).padStart(2, '0'), { x: 12.32, y: 7.08, w: 0.6, h: 0.25, fontFace: 'Aptos', fontSize: 8, color: C.muted, align: 'right', margin: 0 });
  slide.addShape(pptx.ShapeType.line, { x: 0.55, y: 6.98, w: 12.25, h: 0, line: { color: C.line, transparency: 35, width: 0.75 } });
}

function title(slide, t, st, idx) {
  addBg(slide);
  slide.addText(t, { x: 0.62, y: 0.48, w: 8.8, h: 0.48, fontFace: 'Aptos Display', fontSize: 23, bold: true, color: C.text, margin: 0 });
  if (st) slide.addText(st, { x: 0.65, y: 1.03, w: 10.5, h: 0.28, fontSize: 9.5, color: C.muted, margin: 0 });
  addFooter(slide, idx);
}

function tag(slide, text, x, y, color=C.cyan, w=1.8) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.33, rectRadius: 0.08, fill: { color, transparency: 88 }, line: { color, transparency: 30, width: 0.8 } });
  slide.addText(text, { x: x+0.10, y: y+0.075, w: w-0.2, h: 0.16, fontSize: 7.2, color, bold: true, align: 'center', margin: 0 });
}

function panel(slide, x, y, w, h, opts={}) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.11, fill: { color: opts.fill || C.panel, transparency: opts.transparency || 0 }, line: { color: opts.line || C.line, width: opts.width || 0.75, transparency: opts.lineTransparency || 0 } });
}

function kpi(slide, label, value, x, y, w, color=C.cyan) {
  panel(slide, x, y, w, 0.88, { fill: C.panel2, line: color, lineTransparency: 35 });
  slide.addText(value, { x: x+0.15, y: y+0.16, w: w-0.3, h: 0.28, fontSize: 17, bold: true, color, align: 'center', margin: 0 });
  slide.addText(label, { x: x+0.15, y: y+0.55, w: w-0.3, h: 0.18, fontSize: 6.5, color: C.muted, align: 'center', margin: 0 });
}

function bullet(slide, items, x, y, w, h, size=12) {
  const runs = [];
  for (const item of items) runs.push({ text: item, options: { bullet: { type: 'bullet' }, breakLine: true } });
  slide.addText(runs, { x, y, w, h, fontFace: 'Aptos', fontSize: size, color: C.text, breakLine: false, fit: 'shrink', paraSpaceAfterPt: 10, margin: 0.05 });
}

function addNotes(slide, lines) {
  if (slide.addNotes) slide.addNotes(lines.join('\n'));
}

function metricValue(metrics, key, fallback='generated') {
  try {
    const obj = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'reports', 'metrics.json')));
    const val = obj.primary_result && obj.primary_result[key];
    if (typeof val === 'number') {
      if (key.includes('accuracy') || key.includes('f1')) return (val*100).toFixed(1)+'%';
      return String(Math.round(val*100)/100);
    }
    if (typeof val === 'string') return val;
    return fallback;
  } catch (_) { return fallback; }
}

function wave(slide, x, y, w, h, color=C.cyan, phase=0) {
  const pts = [];
  const n = 32;
  for (let i=0;i<n;i++) {
    const px = x + w*i/(n-1);
    const py = y + h/2 + Math.sin(i*0.55+phase)*h*0.34 + Math.sin(i*1.25+phase)*h*0.08;
    pts.push([px, py]);
  }
  for (let i=0;i<n-1;i++) {
    slide.addShape(pptx.ShapeType.line, { x: pts[i][0], y: pts[i][1], w: pts[i+1][0]-pts[i][0], h: pts[i+1][1]-pts[i][1], line: { color, width: 1.3, transparency: 5 } });
  }
}

// 1
{
  const slide = pptx.addSlide(); addBg(slide);
  tag(slide, 'SECURITE IOT', 0.7, 0.55, C.cyan, 1.55);
  tag(slide, 'PRIVACY', 2.45, 0.55, C.violet, 1.25);
  slide.addText('PrivIMU', { x: 0.7, y: 1.65, w: 5.1, h: 0.75, fontFace: 'Aptos Display', fontSize: 44, bold: true, color: C.text, margin: 0 });
  slide.addText('Motion Anonymity Attack', { x: 0.75, y: 2.45, w: 6.0, h: 0.35, fontSize: 19, color: C.cyan, bold: true, margin: 0 });
  slide.addText('Can anonymous accelerometer + gyroscope traces reveal user identity?', { x: 0.78, y: 3.03, w: 6.4, h: 0.35, fontSize: 13, color: C.muted, margin: 0 });
  // phone card
  panel(slide, 8.15, 0.82, 3.55, 5.45, { fill: '0F172A', line: C.cyan, lineTransparency: 30 });
  slide.addShape(pptx.ShapeType.roundRect, { x: 9.18, y: 1.22, w: 1.5, h: 0.12, rectRadius: 0.03, fill: { color: C.line }, line: { color: C.line } });
  wave(slide, 8.55, 2.0, 2.9, 0.95, C.cyan, 0.0);
  wave(slide, 8.55, 3.0, 2.9, 0.85, C.violet, 1.2);
  wave(slide, 8.55, 4.0, 2.9, 0.75, C.green, 2.1);
  slide.addText('anonymous.csv', { x: 8.6, y: 5.22, w: 2.7, h: 0.2, fontSize: 8, color: C.muted, align: 'center', margin: 0 });
  slide.addShape(pptx.ShapeType.line, { x: 6.45, y: 3.6, w: 1.2, h: 0, line: { color: C.cyan, width: 2, beginArrowType: 'none', endArrowType: 'triangle' } });
  panel(slide, 4.8, 3.15, 1.6, 1.05, { fill: C.panel2, line: C.cyan, lineTransparency: 15 });
  slide.addText('ML\nattacker', { x: 5.05, y: 3.34, w: 1.1, h: 0.45, fontSize: 13, bold: true, color: C.text, align: 'center', valign: 'mid', margin: 0 });
  slide.addText('Deliverables: repo + Colab + Streamlit + slides + report + metrics.json', { x: 0.75, y: 5.8, w: 6.8, h: 0.28, fontSize: 10, color: C.text, margin: 0 });
  addFooter(slide, 1);
  addNotes(slide, [
    'Nous presentons PrivIMU, un mini-lab de securite IoT qui teste si les traces IMU anonymes peuvent devenir des quasi-identifiants comportementaux.',
    'Le message cle est simple: pas besoin de nom, email ou visage pour creer une fuite de confidentialite.',
  ]);
}

// 2
{
  const slide = pptx.addSlide(); title(slide, 'Pourquoi les IMU sont un enjeu IoT', 'Les capteurs de mouvement sont discrets, permanents et souvent consideres comme peu sensibles.', 2);
  const xs = [0.9, 3.3, 5.7, 8.1, 10.5];
  const labels = ['Smartphone', 'Wearable', 'Health app', 'Sport app', 'Mobility'];
  const icons = ['phone', 'watch', 'heart', 'run', 'map'];
  labels.forEach((l,i)=>{
    panel(slide, xs[i], 2.0, 1.65, 1.55, { fill: C.panel2, line: [C.cyan,C.violet,C.green,C.amber,C.blue][i], lineTransparency: 45 });
    slide.addText(icons[i], { x: xs[i]+0.15, y: 2.25, w: 1.35, h: 0.25, fontSize: 12, color: [C.cyan,C.violet,C.green,C.amber,C.blue][i], bold: true, align: 'center', margin: 0 });
    slide.addText(l, { x: xs[i]+0.12, y: 2.82, w: 1.4, h: 0.22, fontSize: 9, color: C.text, bold: true, align: 'center', margin: 0 });
  });
  panel(slide, 1.2, 4.35, 10.9, 1.0, { fill: '0F172A', line: C.red, lineTransparency: 50 });
  slide.addText('Problem: these traces are often shared as "anonymous" telemetry.', { x: 1.55, y: 4.65, w: 10.2, h: 0.25, fontSize: 16, bold: true, color: C.text, align: 'center', margin: 0 });
  addNotes(slide, ['Les IMU sont partout dans les objets connectes. Le risque vient du fait que la collecte peut etre invisible pour l’utilisateur et qualifiee a tort de faible risque.']);
}

// 3
{
  const slide = pptx.addSlide(); title(slide, 'Question scientifique', 'Anonyme ne veut pas dire non re-identifiable.', 3);
  panel(slide, 0.9, 1.75, 5.25, 4.25, { fill: C.panel2, line: C.cyan, lineTransparency: 35 });
  slide.addText('Signal IMU', { x: 1.25, y: 2.05, w: 2, h: 0.25, fontSize: 18, color: C.cyan, bold: true, margin: 0 });
  wave(slide, 1.25, 2.65, 4.15, 0.65, C.cyan, 0.4);
  wave(slide, 1.25, 3.45, 4.15, 0.65, C.violet, 1.7);
  wave(slide, 1.25, 4.25, 4.15, 0.65, C.green, 2.8);
  slide.addText('No name. No email. No face.', { x: 1.25, y: 5.2, w: 4.4, h: 0.22, fontSize: 12, color: C.muted, margin: 0 });
  panel(slide, 7.15, 1.75, 5.1, 4.25, { fill: C.panel2, line: C.red, lineTransparency: 35 });
  slide.addText('Identity posterior', { x: 7.5, y: 2.05, w: 3, h: 0.25, fontSize: 18, color: C.red, bold: true, margin: 0 });
  ['Subject 07','Subject 12','Subject 03'].forEach((l,i)=>{
    const yy=2.75+i*0.73; const ww=[3.4,2.25,1.6][i];
    slide.addText(l, { x: 7.55, y: yy, w: 1.7, h: 0.2, fontSize: 10, color: C.text, margin: 0 });
    slide.addShape(pptx.ShapeType.rect, { x: 9.4, y: yy+0.03, w: ww, h: 0.18, fill: { color: [C.red,C.amber,C.violet][i] }, line: { color: [C.red,C.amber,C.violet][i] } });
  });
  slide.addText('Hypothesis: motion traces act as behavioral quasi-identifiers.', { x: 7.55, y: 5.2, w: 4.5, h: 0.34, fontSize: 12, color: C.muted, margin: 0 });
  slide.addShape(pptx.ShapeType.line, { x: 6.25, y: 3.75, w: 0.83, h: 0, line: { color: C.cyan, width: 2, endArrowType: 'triangle' } });
  addNotes(slide, ['La question scientifique: un signal qui ne porte aucun champ identite peut-il quand meme pointer vers une personne parmi 24?']);
}

// 4
{
  const slide = pptx.addSlide(); title(slide, 'Threat model', 'Un attaquant modeste, pas un laboratoire militaire.', 4);
  const cards = [
    ['1', 'Enrollment data', 'Traces publiques ou historiques pour apprendre les signatures.'],
    ['2', 'Anonymous IMU CSV', 'Acceleration + gyroscope-derived signal, no explicit ID.'],
    ['3', 'Classifier', 'Random Forest or 1D-CNN, CPU-friendly.'],
    ['4', 'Top-3 identity', 'Posterior over 24 enrolled subjects.'],
  ];
  cards.forEach((c,i)=>{
    const x = 0.85 + i*3.05;
    panel(slide, x, 2.1, 2.45, 2.75, { fill: C.panel2, line: [C.cyan,C.violet,C.green,C.red][i], lineTransparency: 40 });
    slide.addText(c[0], { x: x+0.17, y: 2.28, w: 0.35, h: 0.35, fontSize: 14, color: C.bg, bold: true, align: 'center', margin: 0, fill: { color: [C.cyan,C.violet,C.green,C.red][i] } });
    slide.addText(c[1], { x: x+0.22, y: 2.9, w: 2.0, h: 0.25, fontSize: 13.5, bold: true, color: C.text, margin: 0 });
    slide.addText(c[2], { x: x+0.22, y: 3.45, w: 2.0, h: 0.72, fontSize: 9.2, color: C.muted, fit: 'shrink', margin: 0 });
    if (i<3) slide.addShape(pptx.ShapeType.line, { x: x+2.52, y: 3.48, w: 0.5, h: 0, line: { color: C.cyan, width: 1.3, transparency: 20, endArrowType: 'triangle' } });
  });
  panel(slide, 2.3, 5.55, 8.8, 0.55, { fill: '0F172A', line: C.amber, lineTransparency: 55 });
  slide.addText('Privacy framing: this is an academic defensive demo, using a public dataset.', { x: 2.5, y: 5.72, w: 8.4, h: 0.18, fontSize: 10.5, color: C.amber, align: 'center', margin: 0 });
  addNotes(slide, ['Le threat model reste realiste: pas de malware, pas d’exfiltration avancee. Juste un fichier de mouvement anonyme et un classifieur.']);
}

// 5
{
  const slide = pptx.addSlide(); title(slide, 'Positionnement scientifique', 'PrivIMU relie HAR, biometrie comportementale et privacy IoT.', 5);
  const circles = [
    [2.9, 3.15, 'HAR', 'activity recognition', C.cyan],
    [6.65, 3.15, 'Behavioral\nbiometrics', 'gait / motion signatures', C.violet],
    [4.75, 4.55, 'Sensor\nprivacy', 'leakage + defenses', C.red],
  ];
  circles.forEach(([x,y,t,sub,col])=>{
    slide.addShape(pptx.ShapeType.ellipse, { x:x-1.45, y:y-1.15, w:2.9, h:2.3, fill:{ color: col, transparency: 86 }, line:{ color: col, width: 1.2, transparency: 25 } });
    slide.addText(t, { x:x-1.05, y:y-0.25, w:2.1, h:0.46, fontSize: 15, bold: true, color: C.text, align:'center', valign:'mid', margin:0 });
    slide.addText(sub, { x:x-1.1, y:y+0.42, w:2.2, h:0.22, fontSize: 8, color: C.muted, align:'center', margin:0 });
  });
  panel(slide, 8.35, 1.85, 3.75, 4.15, { fill: C.panel2, line: C.line });
  slide.addText('Our gap', { x: 8.75, y: 2.25, w: 2.5, h: 0.24, fontSize: 18, bold: true, color: C.green, margin: 0 });
  bullet(slide, [
    'Closed-set identity attack on MotionSense',
    'Reproducible pipeline, not only slides',
    'Live demo with privacy entropy',
    'Mitigation discussion: noise, minimization, edge, DP',
  ], 8.65, 2.88, 3.1, 2.4, 10.2);
  addNotes(slide, ['Cette slide evite l’effet tutoriel. Elle montre que le projet s’inscrit dans trois lignes de recherche etablies.']);
}

// 6
{
  const slide = pptx.addSlide(); title(slide, 'Dataset: MotionSense', 'Public IMU dataset collected from smartphone motion sensors.', 6);
  kpi(slide, 'data subjects', '24', 0.95, 1.65, 2.05, C.cyan);
  kpi(slide, 'activities', '6', 3.25, 1.65, 2.05, C.violet);
  kpi(slide, 'sampling', '50 Hz', 5.55, 1.65, 2.05, C.green);
  kpi(slide, 'device', 'iPhone', 7.85, 1.65, 2.05, C.amber);
  kpi(slide, 'placement', 'pocket', 10.15, 1.65, 2.05, C.blue);
  panel(slide, 0.95, 3.25, 5.8, 2.45, { fill: C.panel2, line: C.line });
  slide.addText('Activities', { x: 1.25, y: 3.55, w: 2.2, h: 0.24, fontSize: 17, bold: true, color: C.text, margin: 0 });
  const acts = ['walking', 'jogging', 'upstairs', 'downstairs', 'sitting', 'standing'];
  acts.forEach((a,i)=> tag(slide, a, 1.2+(i%3)*1.75, 4.08+Math.floor(i/3)*0.6, [C.cyan,C.green,C.violet,C.blue,C.amber,C.red][i], 1.45));
  panel(slide, 7.15, 3.25, 5.1, 2.45, { fill: C.panel2, line: C.line });
  slide.addText('Channels used by PrivIMU', { x: 7.45, y: 3.55, w: 3.0, h: 0.24, fontSize: 17, bold: true, color: C.text, margin: 0 });
  bullet(slide, ['rotationRate.x/y/z', 'userAcceleration.x/y/z', '1-second windows with 50% overlap'], 7.45, 4.1, 4.2, 1.2, 10.5);
  addNotes(slide, ['MotionSense est parfait pour notre histoire: 24 sujets, six activites, telephone en poche, 50Hz, et des signaux de mouvement exploitables.']);
}

// 7
{
  const slide = pptx.addSlide(); title(slide, 'Pipeline reproductible', 'Chaque chiffre doit venir du code et de reports/metrics.json.', 7);
  const boxes = [
    ['download.py','MotionSense ZIP'], ['data.py','CSV -> arrays'], ['features.py','windows + features'], ['train.py','RF / CNN'], ['evaluate.py','metrics + gates']
  ];
  boxes.forEach((b,i)=>{
    const x = 0.75 + i*2.47;
    panel(slide, x, 2.35, 1.95, 1.25, { fill: C.panel2, line: [C.cyan,C.blue,C.violet,C.green,C.red][i], lineTransparency: 35 });
    slide.addText(b[0], { x:x+0.15, y:2.65, w:1.65, h:0.22, fontSize: 12, bold: true, color:C.text, align:'center', margin:0 });
    slide.addText(b[1], { x:x+0.15, y:3.03, w:1.65, h:0.18, fontSize: 8, color:C.muted, align:'center', margin:0 });
    if (i<boxes.length-1) slide.addShape(pptx.ShapeType.line, { x:x+1.98, y:2.98, w:0.45, h:0, line:{ color:C.cyan, width:1.2, transparency:20, endArrowType:'triangle' } });
  });
  panel(slide, 2.0, 4.75, 9.3, 0.82, { fill: '0F172A', line: C.green, lineTransparency: 35 });
  slide.addText('Rule: no manual metric in slides or report. Source of truth = reports/metrics.json', { x: 2.25, y: 5.02, w: 8.8, h: 0.2, fontSize: 13, bold: true, color: C.green, align: 'center', margin: 0 });
  addNotes(slide, ['C’est une slide de vente de l’effort: le prof peut cloner le repo, relancer le pipeline et verifier les chiffres.']);
}

// 8
{
  const slide = pptx.addSlide(); title(slide, 'Preprocessing and features', 'From raw time-series to identity-classification features.', 8);
  panel(slide, 0.85, 1.75, 4.1, 4.55, { fill: C.panel2, line: C.cyan, lineTransparency: 40 });
  slide.addText('Windowing', { x: 1.18, y: 2.05, w: 1.7, h: 0.25, fontSize: 17, bold: true, color: C.cyan, margin: 0 });
  wave(slide, 1.2, 2.65, 3.25, 0.8, C.cyan, 0.3);
  slide.addShape(pptx.ShapeType.rect, { x: 1.65, y: 2.55, w: 1.15, h: 1.0, fill: { color: C.cyan, transparency: 88 }, line: { color: C.cyan, width: 1.2 } });
  slide.addText('50 samples\n= 1s', { x: 1.72, y: 3.75, w: 1.0, h: 0.38, fontSize: 9, color: C.text, align: 'center', margin: 0 });
  slide.addShape(pptx.ShapeType.rect, { x: 2.25, y: 2.55, w: 1.15, h: 1.0, fill: { color: C.violet, transparency: 88 }, line: { color: C.violet, width: 1.2 } });
  slide.addText('50% overlap', { x: 2.23, y: 4.25, w: 1.25, h: 0.2, fontSize: 9, color: C.muted, align: 'center', margin: 0 });
  panel(slide, 5.45, 1.75, 3.0, 4.55, { fill: C.panel2, line: C.violet, lineTransparency: 40 });
  slide.addText('Feature set', { x: 5.8, y: 2.05, w: 1.9, h: 0.25, fontSize: 17, bold: true, color: C.violet, margin: 0 });
  bullet(slide, ['mean / std / min / max', 'RMS and range', 'skewness / kurtosis', 'spectral entropy', 'energy-like descriptors'], 5.8, 2.65, 2.4, 2.4, 10.0);
  panel(slide, 8.95, 1.75, 3.45, 4.55, { fill: C.panel2, line: C.green, lineTransparency: 40 });
  slide.addText('Models', { x: 9.3, y: 2.05, w: 1.9, h: 0.25, fontSize: 17, bold: true, color: C.green, margin: 0 });
  bullet(slide, ['Random Forest baseline', '1D-CNN extension', 'Top-1 / Top-3 metrics', 'latency per window'], 9.3, 2.75, 2.8, 1.9, 10.2);
  addNotes(slide, ['La methode reste simple et defendable: des fenetres de 1 seconde, normalisation par fenetre, puis features statistiques et spectrales.']);
}

// 9
{
  const slide = pptx.addSlide(); title(slide, 'Evaluation protocol', 'Avoiding leakage is as important as the classifier.', 9);
  panel(slide, 0.95, 1.65, 5.5, 4.85, { fill: C.panel2, line: C.cyan, lineTransparency: 35 });
  slide.addText('Split strategy', { x: 1.3, y: 2.05, w: 2.4, h: 0.25, fontSize: 18, bold: true, color: C.cyan, margin: 0 });
  slide.addText('Group-based split by activity/trial prevents adjacent windows from the same trial leaking across train/test.', { x: 1.3, y: 2.65, w: 4.55, h: 0.9, fontSize: 12.2, color: C.text, fit: 'shrink', margin: 0 });
  slide.addText('Bad split', { x: 1.35, y: 4.0, w: 1.2, h: 0.2, fontSize: 10, color: C.red, bold: true, margin: 0 });
  slide.addText('window 1 | window 2 | window 3 mixed randomly', { x: 2.45, y: 4.0, w: 3.3, h: 0.2, fontSize: 8.5, color: C.muted, margin: 0 });
  slide.addText('Good split', { x: 1.35, y: 4.65, w: 1.2, h: 0.2, fontSize: 10, color: C.green, bold: true, margin: 0 });
  slide.addText('whole trial held out as evaluation group', { x: 2.45, y: 4.65, w: 3.2, h: 0.2, fontSize: 8.5, color: C.muted, margin: 0 });
  panel(slide, 7.05, 1.65, 5.1, 4.85, { fill: C.panel2, line: C.violet, lineTransparency: 35 });
  slide.addText('Metrics', { x: 7.4, y: 2.05, w: 1.6, h: 0.25, fontSize: 18, bold: true, color: C.violet, margin: 0 });
  bullet(slide, ['Top-1 accuracy', 'Top-3 accuracy', 'Macro-F1', 'Confusion matrix 24x24', 'Per-subject F1', 'Privacy entropy leakage', 'Latency / window'], 7.4, 2.65, 4.1, 3.2, 11.0);
  addNotes(slide, ['Le split est un point que le jury technique peut attaquer. Ici, on montre explicitement qu’on evite la fuite trial-vers-trial.']);
}

// 10
{
  const slide = pptx.addSlide(); title(slide, 'Demo architecture', 'The demo turns privacy leakage into something visible.', 10);
  const b = [
    ['Upload CSV', 'MotionSense-like file'], ['Plot signal', 'accel + gyro channels'], ['Predict', 'Top-3 subject IDs'], ['Defend', 'Gaussian noise slider']
  ];
  b.forEach((item,i)=>{
    const x=0.95+i*3.0;
    panel(slide, x, 2.25, 2.25, 2.15, { fill: C.panel2, line:[C.cyan,C.violet,C.red,C.green][i], lineTransparency:35 });
    slide.addText(item[0], { x:x+0.18, y:2.65, w:1.9, h:0.25, fontSize:14.5, bold:true, color:C.text, align:'center', margin:0 });
    slide.addText(item[1], { x:x+0.2, y:3.25, w:1.85, h:0.4, fontSize:9, color:C.muted, align:'center', margin:0 });
    if (i<3) slide.addShape(pptx.ShapeType.line, { x:x+2.3, y:3.3, w:0.6, h:0, line:{ color:C.cyan, width:1.3, transparency:20, endArrowType:'triangle' } });
  });
  panel(slide, 2.55, 5.15, 8.2, 0.65, { fill: '0F172A', line: C.amber, lineTransparency: 50 });
  slide.addText('Fallback mode keeps the UI clickable before training; real predictions use models/rf.joblib.', { x: 2.8, y: 5.35, w: 7.7, h: 0.18, fontSize: 10.5, color: C.amber, align: 'center', margin: 0 });
  addNotes(slide, ['Cette slide prepare la demo. On explique le flux sans entrer dans le code: upload, visualisation, prediction, defense.']);
}

// 11
{
  const slide = pptx.addSlide(); title(slide, 'Live attack: from signal to Top-3 identity', 'The signal has no explicit identity field.', 11);
  panel(slide, 0.85, 1.6, 7.0, 4.8, { fill: C.panel2, line: C.line });
  slide.addText('Anonymous IMU signal', { x: 1.15, y: 1.95, w: 2.8, h: 0.25, fontSize: 16, bold: true, color: C.text, margin: 0 });
  wave(slide, 1.2, 2.65, 6.2, 0.65, C.cyan, 0.1);
  wave(slide, 1.2, 3.45, 6.2, 0.65, C.violet, 1.3);
  wave(slide, 1.2, 4.25, 6.2, 0.65, C.green, 2.5);
  slide.addText('rotationRate.x/y/z + userAcceleration.x/y/z', { x: 1.2, y: 5.45, w: 4.8, h: 0.2, fontSize: 9, color: C.muted, margin: 0 });
  panel(slide, 8.4, 1.6, 3.9, 4.8, { fill: C.panel2, line: C.red, lineTransparency: 35 });
  slide.addText('Top-3 posterior', { x: 8.75, y: 1.95, w: 2.5, h: 0.25, fontSize: 16, bold: true, color: C.red, margin: 0 });
  const bars=[['Subject 07','0.62',2.85,2.45,C.red],['Subject 12','0.18',3.55,1.15,C.amber],['Subject 03','0.08',4.25,0.58,C.violet]];
  bars.forEach(([l,v,y,w,c])=>{
    slide.addText(l, { x:8.75, y:y, w:1.45, h:0.2, fontSize:9.5, color:C.text, margin:0 });
    slide.addShape(pptx.ShapeType.rect, { x:10.15, y:y+0.03, w, h:0.17, fill:{color:c}, line:{color:c} });
    slide.addText(v, { x:11.55, y:y, w:0.5, h:0.18, fontSize:8, color:C.muted, align:'right', margin:0 });
  });
  slide.addText('Replace example bars with live app output during the presentation.', { x: 8.75, y: 5.45, w: 2.9, h: 0.34, fontSize: 9, color: C.muted, margin: 0 });
  addNotes(slide, ['Pendant la soutenance, cette slide doit devenir une demo live. Le moment fort: le fichier est anonyme mais l’app propose un Top-3 de sujets.']);
}

// 12
{
  const slide = pptx.addSlide(); title(slide, 'Defense demo: perturbation vs leakage', 'A simple noise slider turns privacy into a measurable trade-off.', 12);
  panel(slide, 0.95, 1.6, 5.5, 4.75, { fill: C.panel2, line: C.green, lineTransparency: 35 });
  slide.addText('Gaussian noise slider', { x:1.3, y:2.0, w:2.8, h:0.25, fontSize:18, bold:true, color:C.green, margin:0 });
  [0,1,2,3].forEach((i)=>{
    const x=1.35+i*1.1;
    slide.addShape(pptx.ShapeType.rect, { x, y:3.15, w:0.75, h:0.12, fill:{color:C.line}, line:{color:C.line} });
    slide.addShape(pptx.ShapeType.ellipse, { x:x+0.28, y:2.98, w:0.26, h:0.26, fill:{color:[C.cyan,C.green,C.amber,C.red][i]}, line:{color:[C.cyan,C.green,C.amber,C.red][i]} });
    slide.addText(['0','0.2','0.5','1.0'][i], { x:x+0.08, y:3.45, w:0.55, h:0.16, fontSize:7.5, color:C.muted, align:'center', margin:0 });
  });
  slide.addText('As sigma increases, identity confidence should drop and posterior entropy should rise.', { x:1.3, y:4.45, w:4.4, h:0.5, fontSize:12, color:C.text, fit:'shrink', margin:0 });
  panel(slide, 7.05, 1.6, 5.1, 4.75, { fill: C.panel2, line: C.violet, lineTransparency: 35 });
  slide.addText('Privacy entropy', { x:7.4, y:2.0, w:2.5, h:0.25, fontSize:18, bold:true, color:C.violet, margin:0 });
  // pseudo curve
  const pts = [[7.65,5.0],[8.4,4.35],[9.2,3.75],[10.1,3.1],[11.3,2.65]];
  for(let i=0;i<pts.length-1;i++) slide.addShape(pptx.ShapeType.line, { x:pts[i][0], y:pts[i][1], w:pts[i+1][0]-pts[i][0], h:pts[i+1][1]-pts[i][1], line:{color:C.violet,width:2} });
  slide.addText('more privacy', { x:10.0, y:2.25, w:1.35, h:0.2, fontSize:8.5, color:C.violet, margin:0 });
  slide.addText('less leakage', { x:7.7, y:5.25, w:1.35, h:0.2, fontSize:8.5, color:C.muted, margin:0 });
  addNotes(slide, ['On ne se contente pas de montrer une attaque. On montre aussi une mitigation pedagogique et on discute ses limites.']);
}

// 13
{
  const slide = pptx.addSlide(); title(slide, 'Results - generated, not invented', 'This slide is refreshed from reports/metrics.json after training.', 13);
  kpi(slide, 'Top-1 accuracy', metricValue('','top1_accuracy','run train-rf'), 0.95, 1.65, 2.4, C.cyan);
  kpi(slide, 'Top-3 accuracy', metricValue('','top3_accuracy','run train-rf'), 3.65, 1.65, 2.4, C.violet);
  kpi(slide, 'Macro-F1', metricValue('','f1_macro','run train-rf'), 6.35, 1.65, 2.4, C.green);
  kpi(slide, 'Latency / window', metricValue('','latency_ms_per_window','run train-rf'), 9.05, 1.65, 2.4, C.amber);
  panel(slide, 1.15, 3.35, 11.0, 2.6, { fill: C.panel2, line: C.line });
  slide.addText('Evidence package', { x:1.5, y:3.75, w:2.5, h:0.25, fontSize:18, bold:true, color:C.text, margin:0 });
  bullet(slide, ['reports/metrics.json = source of truth', 'reports/confusion_matrix.png', 'reports/per_subject_f1.png', 'reports/privacy_entropy_curve.png', 'commit message includes Verified-By'], 1.5, 4.35, 5.2, 1.3, 10.7);
  panel(slide, 7.45, 4.05, 3.95, 0.78, { fill: '0F172A', line: C.red, lineTransparency: 40 });
  slide.addText('No manual metric', { x:7.65, y:4.28, w:3.55, h:0.22, fontSize:16, bold:true, color:C.red, align:'center', margin:0 });
  addNotes(slide, ['Cette slide devra etre regeneree apres entrainement. On ne met jamais un chiffre que le fichier metrics.json ne contient pas.']);
}

// 14
{
  const slide = pptx.addSlide(); title(slide, 'Limits and mitigations', 'A strong project is honest about its assumptions.', 14);
  panel(slide, 0.95, 1.65, 5.6, 4.9, { fill: C.panel2, line: C.red, lineTransparency: 40 });
  slide.addText('Limits', { x:1.3, y:2.05, w:1.6, h:0.25, fontSize:18, bold:true, color:C.red, margin:0 });
  bullet(slide, ['Closed-set identification among enrolled subjects', 'MotionSense has 24 subjects', 'Phone-in-pocket setting', 'Dataset differs from every real deployment', 'Noise defense is pedagogical, not a formal guarantee'], 1.3, 2.75, 4.6, 2.9, 11);
  panel(slide, 7.0, 1.65, 5.25, 4.9, { fill: C.panel2, line: C.green, lineTransparency: 40 });
  slide.addText('Mitigations', { x:7.35, y:2.05, w:2.0, h:0.25, fontSize:18, bold:true, color:C.green, margin:0 });
  bullet(slide, ['Data minimization', 'On-device inference', 'Purpose limitation', 'Federated learning', 'Differential privacy for time-series', 'Auditable retention policy'], 7.35, 2.75, 4.3, 3.0, 11);
  addNotes(slide, ['L’objectif est un ton academique neutre: on demontre la fuite, puis on presente les limites et les pistes de mitigation.']);
}

// 15
{
  const slide = pptx.addSlide(); addBg(slide);
  slide.addText('Takeaway', { x:0.75, y:0.75, w:3.2, h:0.5, fontSize:28, bold:true, color:C.text, margin:0 });
  slide.addText('Anonymous motion data can still be privacy-sensitive.', { x:0.78, y:1.55, w:7.8, h:0.45, fontSize:20, bold:true, color:C.cyan, margin:0 });
  slide.addText('PrivIMU is delivered as a reproducible mini-lab: repo, Colab, Streamlit demo, report, slides, tests and generated metrics.', { x:0.8, y:2.35, w:6.5, h:0.8, fontSize:13, color:C.text, fit:'shrink', margin:0 });
  panel(slide, 0.85, 4.0, 3.2, 1.55, { fill:C.panel2, line:C.cyan, lineTransparency:35 });
  slide.addImage({ path: path.join(__dirname, 'assets', 'qr_github.png'), x:1.05, y:4.22, w:0.9, h:0.9 });
  slide.addText('GitHub repo\ngithub.com/akiroussama/PrivIMU', { x:2.12, y:4.42, w:1.75, h:0.45, fontSize:8.5, color:C.text, margin:0 });
  panel(slide, 4.55, 4.0, 3.2, 1.55, { fill:C.panel2, line:C.violet, lineTransparency:35 });
  slide.addImage({ path: path.join(__dirname, 'assets', 'qr_colab.png'), x:4.75, y:4.22, w:0.9, h:0.9 });
  slide.addText('Google Colab\nreproduce results', { x:5.82, y:4.42, w:1.5, h:0.45, fontSize:8.5, color:C.text, margin:0 });
  panel(slide, 8.25, 4.0, 3.2, 1.55, { fill:C.panel2, line:C.green, lineTransparency:35 });
  slide.addImage({ path: path.join(__dirname, 'assets', 'qr_streamlit.png'), x:8.45, y:4.22, w:0.9, h:0.9 });
  slide.addText('Streamlit demo\nprivimu.streamlit.app', { x:9.52, y:4.42, w:1.5, h:0.45, fontSize:8.5, color:C.text, margin:0 });
  addFooter(slide, 15);
  addNotes(slide, ['Conclusion: le projet ne vend pas seulement un resultat, il vend un effort reproductible, deployable et responsable.']);
}

pptx.writeFile({ fileName: path.join(__dirname, 'PrivIMU_final.pptx') });
