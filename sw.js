/* Photo Tools offline support: keeps the apps, icons and fonts on the device so they open without internet */
const VERSION='4ebedb0134cf';
const APP='photo-tools-app-'+VERSION, FONTS='photo-tools-fonts-v1';
/* the background remover's files (about 13 MB) are kept apart, only fetched once, and survive app updates */
const CUTOUT='photo-tools-cutout-1.1.0';
const FILES=['./','index.html','share.html','photo-frame-studio.html','photo-splitter.html','chat-reel.html','metadata-scrubber.html','video-layers.html','manifest.webmanifest',
  'icons/icon-192.png','icons/icon-512.png','icons/icon-maskable-192.png','icons/icon-maskable-512.png','icons/icon-180.png','icons/favicon-32.png'];
const FONT_CSS=[
 "https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Anton&family=Archivo+Black&family=Bangers&family=Bebas+Neue&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,700;1,6..96,400&family=Bowlby+One&family=Caveat:wght@600&family=Cinzel:wght@700&family=Comic+Neue:ital,wght@0,700;1,700&family=DM+Serif+Display:ital@0;1&family=Familjen+Grotesk:wght@400;500;600&family=Josefin+Sans:wght@600&family=Jost:wght@400;500&family=Kalam:wght@700&family=Luckiest+Guy&family=Montserrat:wght@600&family=Oswald:wght@400;500;700&family=Permanent+Marker&family=Playfair+Display:ital,wght@0,900;1,700&family=Roboto:wght@400;500&family=Shadows+Into+Light&family=Share+Tech+Mono&family=Shrikhand&family=Unbounded:wght@600&family=UnifrakturMaguntia&family=VT323&display=swap",
 "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=Unbounded:wght@600&display=swap",
 "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600&family=Roboto:wght@400;500&family=Unbounded:wght@600&display=swap",
 "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600&family=Unbounded:wght@600&display=swap",
 "https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=Unbounded:wght@600&family=Anton&family=Bebas+Neue&family=Playfair+Display:ital,wght@0,700;1,700&family=DM+Serif+Display:ital@0;1&family=Permanent+Marker&family=Caveat:wght@700&family=Pacifico&family=Bangers&family=Fredoka:wght@600&family=Special+Elite&family=Space+Mono:ital,wght@0,700;1,700&display=swap"
];

self.addEventListener('install',e=>{e.waitUntil((async()=>{
  const c=await caches.open(APP);
  await c.addAll(FILES.map(u=>new Request(u,{cache:'reload'})));
  try{await cacheFonts();}catch(err){}
  await self.skipWaiting();
})());});

/* fetch each font stylesheet and the Latin font files it points to */
async function cacheFonts(){
  const c=await caches.open(FONTS);
  await Promise.all(FONT_CSS.map(async href=>{try{
    if(await c.match(href))return;
    const r=await fetch(href,{mode:'cors'});if(!r.ok)return;
    const css=await r.clone().text();await c.put(href,r);
    const urls=new Set(),re=/\/\*\s*([\w-]+)\s*\*\/\s*@font-face\s*\{[^}]*?url\((https:[^)]+)\)/g;let m;
    while((m=re.exec(css)))if(m[1]==='latin'||m[1]==='latin-ext')urls.add(m[2]);
    if(!urls.size)(css.match(/url\((https:[^)]+)\)/g)||[]).forEach(u=>urls.add(u.slice(4,-1)));
    await Promise.all([...urls].map(async u=>{try{if(await c.match(u))return;const fr=await fetch(u,{mode:'cors'});if(fr.ok)await c.put(u,fr);}catch(e){}}));
  }catch(e){}}));
}

self.addEventListener('activate',e=>{e.waitUntil((async()=>{
  for(const k of await caches.keys())if(k.startsWith('photo-tools-')&&k!==APP&&k!==FONTS&&k!==CUTOUT)await caches.delete(k);
  await self.clients.claim();
})());});

self.addEventListener('fetch',e=>{
  const req=e.request;
  if(req.method==='POST'&&new URL(req.url).pathname.endsWith('/share.html')){e.respondWith(receiveShare(req));return;}
  if(req.method!=='GET')return;
  const url=new URL(req.url);
  if(url.origin==='https://fonts.googleapis.com'||url.origin==='https://fonts.gstatic.com'){e.respondWith(fontFirst(req));return;}
  if(url.origin!==self.location.origin)return;
  if(url.pathname.includes('/vendor/')){e.respondWith(vendorFile(req,e));return;}
  e.respondWith(appFile(req,e));
});
async function fontFirst(req){
  const c=await caches.open(FONTS);
  const hit=(await c.match(req,{ignoreVary:true}))||(await c.match(req.url,{ignoreVary:true}));
  if(hit)return hit;
  try{const r=await fetch(req);if(r&&(r.ok||r.type==='opaque'))c.put(req,r.clone());return r;}
  catch(err){return new Response('',{status:504});}
}
async function vendorFile(req,e){
  const c=await caches.open(CUTOUT);const hit=await c.match(req,{ignoreSearch:true});if(hit)return hit;
  try{const r=await fetch(req);if(r&&r.ok&&r.type==='basic')e.waitUntil(c.put(req,r.clone()).catch(()=>{}));return r;}
  catch(err){return new Response('You’re offline and the background remover isn’t saved on this device yet.',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}});}
}
/* show the saved copy straight away, and quietly fetch a newer one for next time */
async function appFile(req,e){
  const c=await caches.open(APP);
  const hit=await c.match(req,{ignoreSearch:true});
  const net=fetch(req).then(r=>{if(r&&r.ok&&r.type==='basic')c.put(req,r.clone());return r;}).catch(()=>null);
  if(hit){e.waitUntil(net);return hit;}
  const r=await net;if(r)return r;
  if(req.mode==='navigation'){const home=await c.match('index.html');if(home)return home;}
  return new Response('You’re offline and this file isn’t saved on this device yet.',{status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}});
}

/* the phone's Share menu sends photos and videos here; keep them for the page that opens next */
async function receiveShare(req){
  try{const fd=await req.formData(),files=fd.getAll('media').filter(f=>f&&typeof f!=='string'&&f.size);
    const c=await caches.open('pt-handoff');for(const k of await c.keys())await c.delete(k);let i=0;
    for(const f of files)await c.put(new Request(new URL('handoff/'+Date.now()+'-'+(i++),self.registration.scope)),new Response(f,{headers:{'content-type':f.type||'application/octet-stream','x-name':encodeURIComponent(f.name||'file')}}));
  }catch(err){}
  return Response.redirect(new URL('share.html?shared=1',self.registration.scope).href,303);
}
