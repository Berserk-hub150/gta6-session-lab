const id=s=>document.getElementById(s),canvas=id("arena"),ctx=canvas.getContext("2d");let token="",position=[50,50],busy=false;
async function post(path,data){const r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});const j=await r.json();if(!r.ok)throw Error(j.error);return j;}
id("join").onclick=async()=>{try{token=(await post("/join",{name:id("name").value})).token;id("join").disabled=true;id("status").textContent="Click the arena to move.";}catch(e){id("status").textContent=e.message;}};
canvas.onclick=e=>{if(!token)return;const b=canvas.getBoundingClientRect();position=[100*(e.clientX-b.left)/b.width,100*(e.clientY-b.top)/b.height];};
async function refresh(){if(busy)return;busy=true;try{const rows=token?await post("/move",{token,x:position[0],y:position[1]}):await (await fetch("/state")).json();
 ctx.clearRect(0,0,480,300);for(const p of rows){const x=p.x*4.8,y=p.y*3;ctx.fillStyle="#ffb58a";ctx.fillRect(x-4,y-4,9,9);ctx.fillStyle="#fff";ctx.fillText(p.name,x+6,y);}}
 catch(e){id("status").textContent=e.message;if(e.message.includes("expired")){token="";id("join").disabled=false;}}finally{busy=false;}}
setInterval(refresh,500);refresh();
