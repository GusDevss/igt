const PARTICLE_COUNT = 5;
const MAX_VELOCITY = 0.7;
const CANVAS_WIDTH = 1920;
const CANVAS_HEIGHT = 400;

class Particle {
    constructor(context) {
        this.x = 0;
        this.y = 0;
        this.xVelocity = 0;
        this.yVelocity = 0;
        this.radius = 5;
        this.context = context;
    }

    draw() {
        if (this.image) {
            this.context.drawImage(this.image, this.x - 128, this.y - 128);
            return;
        }
        this.context.beginPath();
        this.context.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        this.context.fillStyle = "rgba(225, 211, 255, 0.50)";
        this.context.fill();
        this.context.closePath();
    }

    update() {
        this.x += this.xVelocity;
        this.y += this.yVelocity;
        if (this.x >= CANVAS_WIDTH || this.x <= 0) this.xVelocity = -this.xVelocity;
        if (this.y >= CANVAS_HEIGHT || this.y <= 0) this.yVelocity = -this.yVelocity;
    }

    setPosition(x, y) {
        this.x = x;
        this.y = y;
    }

    setVelocity(x, y) {
        this.xVelocity = x;
        this.yVelocity = y;
    }

    setImage(image) {
        this.image = image;
    }
}

function generateRandom(min, max) {
    return Math.random() * (max - min) + min;
}

function init(canvas) {
    canvas.width = CANVAS_WIDTH;
    canvas.height = CANVAS_HEIGHT;
    const context = canvas.getContext('2d');
    const particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const particle = new Particle(context);
        particle.setPosition(generateRandom(0, CANVAS_WIDTH), generateRandom(0, CANVAS_HEIGHT));
        particle.setVelocity(generateRandom(-MAX_VELOCITY, MAX_VELOCITY), generateRandom(-MAX_VELOCITY, MAX_VELOCITY));
        particles.push(particle);
    }
    loadAndAnimateImage(particles, context);
}

function loadAndAnimateImage(particles, context) {
    const imageObj = new Image();
    imageObj.onload = function () {
        particles.forEach(particle => {
            particle.setImage(imageObj);
        });
        animate(particles, context);
    };
    imageObj.src = "https://rawgit.com/marcobiedermann/playground/master/three.js/smoke-particles/dist/assets/images/clouds.png";
}

function draw(particles, context) {
    context.fillStyle = "rgba(0, 0, 0, 0.5)";
    context.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    particles.forEach(particle => {
        particle.draw();
    });
}

function update(particles) {
    particles.forEach(particle => {
        particle.update();
    });
}

function animate(particles, context) {
    update(particles);
    draw(particles, context);
    requestAnimationFrame(() => animate(particles, context));
}

document.addEventListener("DOMContentLoaded", () => {
    const canvases = document.querySelectorAll('.smoke-canvas');
    canvases.forEach(canvas => {
        init(canvas);
    });
});
