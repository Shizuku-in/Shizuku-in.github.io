document.addEventListener("DOMContentLoaded",()=>{const o=t=>{t.addEventListener("load",()=>{if(t.getAttribute("data-src")&&t.src===""){t.src=t.getAttribute("data-src")}t.classList.add("loaded")});if(t.complete){t.dispatchEvent(new Event("load"))}};const t={root:null,rootMargin:"0px",threshold:.1};const e=new IntersectionObserver((t,n)=>{t.forEach(t=>{const e=t.target;if(t.isIntersecting){o(e);n.unobserve(e)}})},t);const n=document.querySelectorAll(".post-content img, .container img");n.forEach(t=>{e.observe(t)})});