document.addEventListener("DOMContentLoaded",function(){const e=localStorage.getItem("r18-consent-timestamp");const t=60*60*1e3;if(e&&Date.now()-e<t){return}const n=document.createElement("div");n.id="r18-overlay";n.style=`
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.925);
        z-index: 9998;
        display: flex;
        align-items: center;
        justify-content: center;
    `;const o=document.createElement("div");o.id="r18-warning-modal";o.style=`
        background: #252d3880;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        max-width: 90%;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        z-index: 9999;
    `;o.innerHTML=`
        <h2 style="font-weight: bold; color: #b7282e">注意</h2>
        <h2>该网页含有 <span style="color: #698aab">R18</span> 内容</h2>
        <button id="r18-yes" style="margin: 10px; padding: 10px 20px; border-radius: 8px;"><span style="font-weight: bold">嗯～</span> <span style="font-family: sans-serif;">( '▽')ψ</span></button>
        <button id="r18-no" style="margin: 10px; padding: 10px 20px; border-radius: 8px;"><span style="font-weight: bold">快放我走！</span> <span style="font-family: sans-serif;">w(ﾟДﾟ)w</span></button>
    `;n.appendChild(o);document.body.appendChild(n);document.getElementById("r18-yes").addEventListener("click",function(){localStorage.setItem("r18-consent-timestamp",Date.now());n.remove();document.body.style.overflow=""});document.getElementById("r18-no").addEventListener("click",function(){window.location.href="https://blog.cya.moe"});document.body.style.overflow="hidden"});