document.addEventListener("DOMContentLoaded",function(){const t=localStorage.getItem("r18-consent-timestamp");const e=60*60*1e3;if(t&&Date.now()-t<e){return}const n=window.innerWidth-document.documentElement.clientWidth;const o=document.createElement("div");o.id="r18-overlay";o.style=`
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
        opacity: 1;
        transition: opacity 0.5s ease;
        backdrop-filter: blur(10px); /* 添加背景模糊效果 */
    `;const d=document.createElement("div");d.id="r18-warning-modal";d.style=`
        background: #252d3880;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        max-width: 90%;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
        z-index: 9999;
        opacity: 1;
        transition: opacity 0.5s ease;
    `;d.innerHTML=`
        <h2 style="font-weight: bold; color: #b7282e">注意</h2>
        <h2>该页面含有 <span style="color: #698aab">R18</span> 内容</h2>
        <button id="r18-yes" style="margin: 10px; padding: 10px 20px; border-radius: 8px;"><span style="font-weight: bold">嗯～</span> <span style="font-family: sans-serif;">( '▽')ψ</span></button>
        <button id="r18-no" style="margin: 10px; padding: 10px 20px; border-radius: 8px;"><span style="font-weight: bold">快放我走！</span> <span style="font-family: sans-serif;">w(ﾟДﾟ)w</span></button>
    `;o.appendChild(d);document.body.appendChild(o);document.getElementById("r18-yes").addEventListener("click",function(){o.style.opacity="0";d.style.opacity="0";setTimeout(function(){localStorage.setItem("r18-consent-timestamp",Date.now());o.remove();document.body.style.overflow="";document.body.style.paddingRight=""},500)});document.getElementById("r18-no").addEventListener("click",function(){window.location.href="https://blog.cya.moe"});document.body.style.overflow="hidden";document.body.style.paddingRight=`${n}px`});