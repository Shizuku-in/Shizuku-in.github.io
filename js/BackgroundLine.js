// 动态背景粒子效果脚本
!function() {
    // 获取配置参数
    function getConfig() {
        const scripts = document.getElementsByTagName("script");
        const lastScript = scripts[scripts.length - 1];
        return {
            zIndex: lastScript.getAttribute("zIndex") || -1,            // zIndex层级
            opacity: lastScript.getAttribute("opacity") || 0.5,         // 不透明度
            color: lastScript.getAttribute("color") || "0,0,0",         // 线条颜色
            count: parseInt(lastScript.getAttribute("count") || 99, 10) // 粒子数量
        };
    }

    // 调整画布大小
    function resizeCanvas() {
        canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
        width = canvas.width;
        height = canvas.height;
    }

    // 绘制粒子和连线
    function drawParticles() {
        context.clearRect(0, 0, width, height);

        const elements = [mouse].concat(particles);

        particles.forEach(particle => {
            particle.x += particle.xa;
            particle.y += particle.ya;

            // 边界反弹
            particle.xa *= (particle.x > width || particle.x < 0) ? -1 : 1;
            particle.ya *= (particle.y > height || particle.y < 0) ? -1 : 1;

            // 绘制粒子
            context.fillRect(particle.x - 0.5, particle.y - 0.5, 1, 1);

            // 绘制连线
            elements.forEach(other => {
                if (particle !== other && other.x !== null && other.y !== null) {
                    const dx = particle.x - other.x;
                    const dy = particle.y - other.y;
                    const distanceSquared = dx * dx + dy * dy;

                    if (distanceSquared < other.max) {
                        const ratio = (other.max - distanceSquared) / other.max;
                        context.beginPath();
                        context.lineWidth = ratio / 2;
                        context.strokeStyle = `rgba(${config.color},${ratio + 0.2})`;
                        context.moveTo(particle.x, particle.y);
                        context.lineTo(other.x, other.y);
                        context.stroke();
                    }
                }
            });

            // 从元素列表中移除当前粒子
            elements.splice(elements.indexOf(particle), 1);
        });

        requestAnimationFrame(drawParticles);
    }

    const canvas = document.createElement("canvas");
    const config = getConfig();
    const context = canvas.getContext("2d");

    let width, height;
    const particles = [];
    const mouse = { x: null, y: null, max: 20000 };

    canvas.style.cssText = `position:fixed;top:0;left:0;z-index:${config.zIndex};opacity:${config.opacity}`;
    document.body.appendChild(canvas);

    resizeCanvas();
    window.onresize = resizeCanvas;

    // 鼠标事件
    window.onmousemove = function(event) {
        mouse.x = event.clientX;
        mouse.y = event.clientY;
    };
    window.onmouseout = function() {
        mouse.x = null;
        mouse.y = null;
    };

    // 创建粒子
    for (let i = 0; i < config.count; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            xa: 2 * Math.random() - 1,
            ya: 2 * Math.random() - 1,
            max: 6000 // 连线的最大距离平方
        });
    }

    // 启动动画
    drawParticles();
}();
