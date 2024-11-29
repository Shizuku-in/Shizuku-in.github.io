!function() {
    function getAttr(element, attribute, defaultValue) {
        return element.getAttribute(attribute) || defaultValue;
    }

    function getByTagName(tag) {
        return document.getElementsByTagName(tag);
    }

    // 初始化配置参数
    function getConfig() {
        var scripts = getByTagName("script"),
            lastScript = scripts[scripts.length - 1];
        return {
            l: scripts.length,                           // 脚本数量
            z: getAttr(lastScript, "zIndex", -1),       // zIndex
            o: getAttr(lastScript, "opacity", 0.5),    // 不透明度
            c: getAttr(lastScript, "color", "0,0,0"),   // 颜色
            n: getAttr(lastScript, "count", 99)         // 粒子数量
        };
    }

    // 设置画布尺寸
    function setCanvasSize() {
        canvas.width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        canvas.height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    }

    // 动画渲染函数
    function animate() {
        ctx.clearRect(0, 0, canvasWidth, canvasHeight); // 清空画布
        var points = [mouse].concat(particles);        // 合并鼠标点和粒子点

        // 遍历所有粒子
        particles.forEach(function(particle) {
            particle.x += particle.xa;
            particle.y += particle.ya;

            // 碰撞边界反弹
            particle.xa *= (particle.x > canvasWidth || particle.x < 0) ? -1 : 1;
            particle.ya *= (particle.y > canvasHeight || particle.y < 0) ? -1 : 1;

            ctx.fillRect(particle.x - 0.5, particle.y - 0.5, 1, 1); // 绘制粒子

            // 连接粒子
            points.forEach(function(target) {
                if (particle !== target && target.x !== null && target.y !== null) {
                    var dx = particle.x - target.x,
                        dy = particle.y - target.y,
                        distanceSquared = dx * dx + dy * dy;

                    if (distanceSquared < target.max) {
                        if (target === mouse && distanceSquared >= target.max / 2) {
                            particle.x -= 0.03 * dx;
                            particle.y -= 0.03 * dy;
                        }

                        var opacity = (target.max - distanceSquared) / target.max;
                        ctx.beginPath();
                        ctx.lineWidth = opacity / 2;
                        ctx.strokeStyle = `rgba(${config.c},${opacity + 0.2})`;
                        ctx.moveTo(particle.x, particle.y);
                        ctx.lineTo(target.x, target.y);
                        ctx.stroke();
                    }
                }
            });
        });

        requestAnimationFrame(animate); // 递归调用
    }

    // 创建画布和上下文
    var canvas = document.createElement("canvas"),
        config = getConfig(),
        canvasId = "c_n" + config.l,
        ctx = canvas.getContext("2d"),
        canvasWidth,
        canvasHeight,
        requestAnimationFrame = window.requestAnimationFrame ||
                                window.webkitRequestAnimationFrame ||
                                window.mozRequestAnimationFrame ||
                                window.oRequestAnimationFrame ||
                                window.msRequestAnimationFrame ||
                                function(callback) {
                                    window.setTimeout(callback, 1000 / 45);
                                },
        random = Math.random,
        mouse = { x: null, y: null, max: 20000 }; // 鼠标虚拟粒子

    canvas.id = canvasId;
    canvas.style.cssText = `position:fixed;top:0;left:0;z-index:${config.z};opacity:${config.o}`;
    getByTagName("body")[0].appendChild(canvas);

    setCanvasSize();
    window.onresize = setCanvasSize;

    // 更新鼠标位置
    window.onmousemove = function(event) {
        event = event || window.event;
        mouse.x = event.clientX;
        mouse.y = event.clientY;
    };

    // 鼠标离开窗口时清除位置
    window.onmouseout = function() {
        mouse.x = null;
        mouse.y = null;
    };

    // 初始化粒子
    var particles = [];
    for (var i = 0; i < config.n; i++) {
        var x = random() * canvasWidth,
            y = random() * canvasHeight,
            xa = 2 * random() - 1,
            ya = 2 * random() - 1;

        particles.push({ x: x, y: y, xa: xa, ya: ya, max: 6000 });
    }

    // 启动动画
    setTimeout(function() {
        animate();
    }, 100);
}();
