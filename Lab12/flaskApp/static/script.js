const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const player = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    size: 20,
    speed: 5,
    dx: 0,
    dy: 0,
    growth: 2, // Tamaño de crecimiento cuando come una bolita
};

const balls = [];
const ballCount = 5;

// Función para crear una bolita en una posición aleatoria
function createBall() {
    const ball = {
        x: Math.random() * (canvas.width - 20) + 10,
        y: Math.random() * (canvas.height - 20) + 10,
        size: 10,
        color: getRandomColor(),
    };
    balls.push(ball);
}

// Crear varias bolitas al inicio
for (let i = 0; i < ballCount; i++) {
    createBall();
}

// Generar un color aleatorio para las bolitas
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Mover al jugador
function movePlayer() {
    player.x += player.dx;
    player.y += player.dy;

    // Limites de la pantalla
    if (player.x < 0) player.x = 0;
    if (player.x + player.size > canvas.width) player.x = canvas.width - player.size;
    if (player.y < 0) player.y = 0;
    if (player.y + player.size > canvas.height) player.y = canvas.height - player.size;
}

// Dibujar al jugador
function drawPlayer() {
    ctx.fillStyle = "#00ff00";
    ctx.fillRect(player.x, player.y, player.size, player.size);
}

// Dibujar bolitas
function drawBalls() {
    balls.forEach(ball => {
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.size, 0, Math.PI * 2);
        ctx.fillStyle = ball.color;
        ctx.fill();
        ctx.closePath();
    });
}

// Detectar colisiones entre el jugador y las bolitas
function detectCollisions() {
    balls.forEach((ball, index) => {
        const distX = Math.abs(player.x + player.size / 2 - ball.x);
        const distY = Math.abs(player.y + player.size / 2 - ball.y);

        if (distX < player.size / 2 + ball.size && distY < player.size / 2 + ball.size) {
            // "Comer" la bolita y crecer
            player.size += player.growth;
            balls.splice(index, 1); // Eliminar la bolita del array
            createBall(); // Crear una nueva bolita en una posición aleatoria
        }
    });
}

// Actualizar el canvas
function update() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawPlayer();
    drawBalls();
    detectCollisions();
    movePlayer();

    requestAnimationFrame(update);
}

// Cambiar dirección según la tecla presionada
function keyDown(e) {
    if (e.key === "ArrowRight" || e.key === "d") {
        player.dx = player.speed;
    } else if (e.key === "ArrowLeft" || e.key === "a") {
        player.dx = -player.speed;
    } else if (e.key === "ArrowUp" || e.key === "w") {
        player.dy = -player.speed;
    } else if (e.key === "ArrowDown" || e.key === "s") {
        player.dy = player.speed;
    }
}

// Detener el movimiento al soltar la tecla
function keyUp(e) {
    if (
        e.key === "ArrowRight" ||
        e.key === "ArrowLeft" ||
        e.key === "d" ||
        e.key === "a"
    ) {
        player.dx = 0;
    } else if (
        e.key === "ArrowUp" ||
        e.key === "ArrowDown" ||
        e.key === "w" ||
        e.key === "s"
    ) {
        player.dy = 0;
    }
}

// Eventos de teclado
document.addEventListener("keydown", keyDown);
document.addEventListener("keyup", keyUp);

// Iniciar el juego
update();
