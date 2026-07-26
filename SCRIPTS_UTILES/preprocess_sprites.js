'use strict';
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');

const SPRITES_DIR='./sprites';
const TARGET_FW=176, TARGET_FH=288;
const THRESHOLD=230;
const SPRITES=['CEO','NICOLE'];

(async()=>{
  console.log('=== PREPROCESANDO Y NORMALIZANDO ESTRUCTURA DE SPRITES ===');
  const b=await chromium.launch({channel:'msedge',headless:true});
  const page=await b.newPage();

  for(const name of SPRITES){
    console.log('\nProcesando '+name+'.png...');
    const result=await page.evaluate(async([n, targetFw, targetFh, thresh])=>{
      const img=new Image();
      img.crossOrigin='anonymous';
      await new Promise((res,rej)=>{
        img.onload=res;
        img.onerror=()=>rej(new Error('No carga sprite: '+n));
        img.src='http://localhost:8080/sprites/'+n+'.png';
      });

      const W=img.naturalWidth, H=img.naturalHeight;
      const cv=document.createElement('canvas');
      cv.width=W; cv.height=H;
      const ctx=cv.getContext('2d');
      ctx.drawImage(img,0,0);

      // Convertir blanco a transparente
      const id=ctx.getImageData(0,0,W,H);
      const d=id.data;
      for(let i=0; i<d.length; i+=4){
        if(d[i]>thresh && d[i+1]>thresh && d[i+2]>thresh){
          d[i+3]=0;
        }
      }
      ctx.putImageData(id,0,0);

      // Algoritmo de BFS para encontrar cada dibujo individual (Blob)
      const visited=new Uint8Array(W*H);
      const blobs=[];

      for(let y=0; y<H; y++){
        for(let x=0; x<W; x++){
          const idx=y*W+x;
          if(visited[idx]) continue;
          visited[idx]=1;

          if(d[idx*4+3]<=10) continue; // pixel transparente

          let minX=x, maxX=x, minY=y, maxY=y, count=0;
          const q=[x,y];
          while(q.length>0){
            const cy=q.pop(), cx=q.pop();
            count++;
            if(cx<minX) minX=cx; if(cx>maxX) maxX=cx;
            if(cy<minY) minY=cy; if(cy>maxY) maxY=cy;

            const nbs=[[cx+1,cy],[cx-1,cy],[cx,cy+1],[cx,cy-1]];
            for(let i=0; i<4; i++){
              const nx=nbs[i][0], ny=nbs[i][1];
              if(nx>=0 && nx<W && ny>=0 && ny<H){
                const nidx=ny*W+nx;
                if(!visited[nidx]){
                  visited[nidx]=1;
                  if(d[nidx*4+3]>10){
                    q.push(nx,ny);
                  }
                }
              }
            }
          }

          // Filtrar ruido menor a 50px de area
          if(count>50){
            blobs.push({minX, maxX, minY, maxY, width: maxX-minX+1, height: maxY-minY+1, count, centerX:(minX+maxX)/2, centerY:(minY+maxY)/2});
          }
        }
      }

      // Ordenar los blobs por FILA (y) y COLUMNA (x)
      // Definir filas separando por umbral Y de ~250px
      const rows=[[], [], [], []];
      blobs.forEach(b=>{
        if(b.centerY < 288) rows[0].push(b);
        else if(b.centerY < 576) rows[1].push(b);
        else if(b.centerY < 864) rows[2].push(b);
        else rows[3].push(b);
      });

      // Ordenar cada fila horizontalmente (de izquierda a derecha)
      rows.forEach(r=>r.sort((a,b)=>a.centerX-b.centerX));

      // Crear nuevo canvas perfecto con grid exacto 12 columnas x 4 filas
      // Cada celda mide exactamente 176x288px
      const outW=12*targetFw, outH=4*targetFh;
      const outCv=document.createElement('canvas');
      outCv.width=outW; outCv.height=outH;
      const outCtx=outCv.getContext('2d');

      const frameCounts=[];
      rows.forEach((rBlobs, rIdx)=>{
        frameCounts.push(rBlobs.length);
        rBlobs.forEach((blob, cIdx)=>{
          if(cIdx>=12) return; // Max 12 frames por fila

          const cellX=cIdx*targetFw;
          const cellY=rIdx*targetFh;

          // Dibujar el personaje perfectamente centrado en su celda 176x288
          // Centrado X = (176 - blob.width)/2
          // Alineado Y = a la base de la celda con padding inferior de 10px (o centrado Y)
          const destX=Math.round(cellX + (targetFw - blob.width)/2);
          const destY=Math.round(cellY + (targetFh - blob.height) - 10);

          outCtx.drawImage(
            cv,
            blob.minX, blob.minY, blob.width, blob.height,
            destX, destY, blob.width, blob.height
          );
        });
      });

      return {
        dataUrl: outCv.toDataURL('image/png'),
        outW, outH,
        frameCounts
      };
    }, [name, TARGET_FW, TARGET_FH, THRESHOLD]);

    console.log('  Frames detectados por fila:', JSON.stringify(result.frameCounts));
    const base64=result.dataUrl.replace(/^data:image\/png;base64,/,'');
    const buf=Buffer.from(base64,'base64');
    const outPath=path.join(SPRITES_DIR, name+'_norm.png');
    fs.writeFileSync(outPath, buf);
    console.log('✓ Guardado sprite normalizado perfecto: '+outPath+' ('+Math.round(buf.length/1024)+'KB)');
  }

  await b.close();
  console.log('\n✓ RE-ESTRUCTURACIÓN COMPLETA DE SPRITES!');
})().catch(e=>{console.error('ERROR:',e.message); process.exit(1);});
