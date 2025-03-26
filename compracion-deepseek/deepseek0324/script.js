document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('dinoCanvas');
    const ctx = canvas.getContext('2d');
    const music = document.getElementById('music');
    const toggleMusicBtn = document.getElementById('toggleMusic');
    const changeColorBtn = document.getElementById('changeColor');
    const changeDanceBtn = document.getElementById('changeDance');
    
    // Variables de estado
    let dinoColor = '#27ae60';
    let danceType = 1;
    let frameCount = 0;
    let musicPlaying = false;
    
    // Colores aleatorios para el dinosaurio
    const colors = [
        '#27ae60', '#e74c3c', '#3498db', '#f39c12', 
        '#9b59b6', '#1abc9c', '#d35400', '#2c3e50'
    ];
    
    // Posiciones de las partes del dinosaurio
    let bodyX = 300;
    let bodyY = 200;
    let headAngle = 0;
    let tailAngle = 0;
    let legAngle1 = 0;
    let legAngle2 = 0;
    let armAngle1 = 0;
    let armAngle2 = 0;
    
    // Controladores de música
    toggleMusicBtn.addEventListener('click', function() {
        if (musicPlaying) {
            music.pause();
            musicPlaying = false;
        } else {
            music.play();
            musicPlaying = true;
        }
    });
    
    // Cambiar color del dinosaurio
    changeColorBtn.addEventListener('click', function() {
        const randomIndex = Math.floor(Math.random() * colors.length);
        dinoColor = colors[randomIndex];
    });
    
    // Cambiar tipo de baile
    changeDanceBtn.addEventListener('click', function() {
        danceType = danceType === 1 ? 2 : 1;
    });
    
    // Función para dibujar el dinosaurio
    function drawDino() {
        // Limpiar canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar cuerpo
        ctx.fillStyle = dinoColor;
        ctx.beginPath();
        ctx.ellipse(bodyX, bodyY, 60, 30, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Dibujar cabeza
        ctx.save();
        ctx.translate(bodyX - 50, bodyY - 30);
        ctx.rotate(headAngle);
        ctx.beginPath();
        ctx.ellipse(30, 0, 30, 20, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Ojo
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(40, -5, 5, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.arc(40, -5, 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Boca
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(45, 5, 10, 0, Math.PI);
        ctx.stroke();
        ctx.restore();
        
        // Dibujar cola
        ctx.save();
        ctx.translate(bodyX + 60, bodyY);
        ctx.rotate(tailAngle);
        
        ctx.fillStyle = dinoColor;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(40, -15);
        ctx.lineTo(80, -10);
        ctx.lineTo(60, 0);
        ctx.lineTo(80, 10);
        ctx.lineTo(40, 15);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
        
        // Dibujar piernas
        // Pierna 1
        ctx.save();
        ctx.translate(bodyX - 20, bodyY + 25);
        ctx.rotate(legAngle1);
        ctx.fillStyle = dinoColor;
        ctx.fillRect(0, 0, 15, 40);
        ctx.restore();
        
        // Pie 1
        ctx.save();
        ctx.translate(bodyX - 20, bodyY + 65);
        ctx.rotate(legAngle1);
        ctx.fillStyle = '#34495e';
        ctx.fillRect(0, 0, 20, 10);
        ctx.restore();
        
        // Pierna 2
        ctx.save();
        ctx.translate(bodyX + 20, bodyY + 25);
        ctx.rotate(legAngle2);
        ctx.fillStyle = dinoColor;
        ctx.fillRect(0, 0, 15, 40);
        ctx.restore();
        
        // Pie 2
        ctx.save();
        ctx.translate(bodyX + 20, bodyY + 65);
        ctx.rotate(legAngle2);
        ctx.fillStyle = '#34495e';
        ctx.fillRect(0, 0, 20, 10);
        ctx.restore();
        
        // Dibujar brazos
        // Brazo 1
        ctx.save();
        ctx.translate(bodyX - 40, bodyY - 10);
        ctx.rotate(armAngle1);
        ctx.fillStyle = dinoColor;
        ctx.fillRect(0, 0, 10, 30);
        ctx.restore();
        
        // Mano 1
        ctx.save();
        ctx.translate(bodyX - 40, bodyY + 20);
        ctx.rotate(armAngle1);
        ctx.fillStyle = '#34495e';
        ctx.beginPath();
        ctx.arc(5, 0, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
        
        // Brazo 2
        ctx.save();
        ctx.translate(bodyX + 10, bodyY - 10);
        ctx.rotate(armAngle2);
        ctx.fillStyle = dinoColor;
        ctx.fillRect(0, 0, 10, 30);
        ctx.restore();
        
        // Mano 2
        ctx.save();
        ctx.translate(bodyX + 10, bodyY + 20);
        ctx.rotate(armAngle2);
        ctx.fillStyle = '#34495e';
        ctx.beginPath();
        ctx.arc(5, 0, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
    
    // Función de animación
    function animate() {
        frameCount++;
        
        // Diferentes patrones de baile
        if (danceType === 1) {
            // Baile 1
            headAngle = Math.sin(frameCount * 0.1) * 0.3;
            tailAngle = Math.sin(frameCount * 0.15) * 0.5;
            legAngle1 = Math.sin(frameCount * 0.2) * 0.4;
            legAngle2 = Math.sin(frameCount * 0.2 + Math.PI) * 0.4;
            armAngle1 = Math.sin(frameCount * 0.15) * 0.5;
            armAngle2 = Math.sin(frameCount * 0.15 + Math.PI) * 0.5;
            bodyY = 200 + Math.sin(frameCount * 0.1) * 10;
        } else {
            // Baile 2 (más salvaje)
            headAngle = Math.sin(frameCount * 0.2) * 0.5;
            tailAngle = Math.sin(frameCount * 0.25) * 0.8;
            legAngle1 = Math.sin(frameCount * 0.3) * 0.6;
            legAngle2 = Math.sin(frameCount * 0.3 + Math.PI) * 0.6;
            armAngle1 = Math.sin(frameCount * 0.25) * 1.0;
            armAngle2 = Math.sin(frameCount * 0.25 + Math.PI) * 1.0;
            bodyY = 200 + Math.sin(frameCount * 0.15) * 15;
            bodyX = 300 + Math.sin(frameCount * 0.1) * 20;
        }
        
        drawDino();
        requestAnimationFrame(animate);
    }
    
    // Iniciar animación
    animate();
});