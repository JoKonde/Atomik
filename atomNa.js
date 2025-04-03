const canvas = document.getElementById("atomCanvas");
const ctx = canvas.getContext("2d");

const nucleus = { x: canvas.width / 2, y: canvas.height / 2, radius: 20 };
const electronOrbits = [40, 80, 120]; // Trois couches électroniques du sodium
const electrons = [];
const speed = 0.05;

// Initialisation des électrons sur leurs orbites
for (let i = 0; i < 2; i++) electrons.push({ orbit: 0, angle: (i * Math.PI) });
for (let i = 0; i < 8; i++) electrons.push({ orbit: 1, angle: (i * (Math.PI / 4)) });
for (let i = 0; i < 1; i++) electrons.push({ orbit: 2, angle: 0 });

function drawNucleus() {
    ctx.beginPath();
    ctx.arc(nucleus.x, nucleus.y, nucleus.radius, 0, Math.PI * 2);
    ctx.fillStyle = "gold";
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = "black";
    ctx.font = "16px Arial";
    ctx.fillText("Na", nucleus.x - 10, nucleus.y + 5);
}

function drawElectrons() {
    electrons.forEach(electron => {
        const orbitRadius = electronOrbits[electron.orbit];
        const x = nucleus.x + orbitRadius * Math.cos(electron.angle);
        const y = nucleus.y + orbitRadius * Math.sin(electron.angle);
        
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = "blue";
        ctx.fill();
        ctx.stroke();
    });
}

function drawOrbits() {
    ctx.strokeStyle = "gray";
    electronOrbits.forEach(radius => {
        ctx.beginPath();
        ctx.arc(nucleus.x, nucleus.y, radius, 0, Math.PI * 2);
        ctx.stroke();
    });
}

function update() {
    electrons.forEach(electron => {
        electron.angle += speed;
    });
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawOrbits();
    drawNucleus();
    drawElectrons();
    update();
    requestAnimationFrame(animate);
}

animate();
