import fs from 'node:fs/promises';
import {Presentation,PresentationFile} from '/Users/dhruvmishra/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const p=Presentation.create({slideSize:{width:1280,height:720}}); const s=p.slides.add();s.background.fill='#F5F7FB';
function tx(text,x,y,w,h,size=28,bold=false,color='#132C48'){const a=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});a.text=text;a.text.style={fontFamily:'Arial',fontSize:size,bold,color};return a;}
tx('Campus WLAN Optimization',70,170,1140,100,54,true);tx('Using Access Point Placement and Network Segmentation',70,280,1100,100,34);tx('SRM Institute of Science and Technology\nFive-member academic capstone team',70,470,1100,100,26);
await fs.writeFile('submission-evidence/build/cover-preview.png',new Uint8Array(await (await p.export({slide:s,format:'png',scale:1})).arrayBuffer()));
await (await PresentationFile.exportPptx(p)).save('submission-evidence/build/cover-draft.pptx');console.log('Bundled presentation runtime works');
