// Three.js Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('canvas-container').appendChild(renderer.domElement);

// Ferrofluid Simulation
const geometry = new THREE.SphereGeometry(1, 128, 128);
const material = new THREE.MeshPhongMaterial({
    color: 0x000000,
    specular: 0x9977d4,
    shininess: 100,
    metalness: 1,
    roughness: 0.5,
});

const ferrofluid = new THREE.Mesh(geometry, material);
scene.add(ferrofluid);

// Lighting
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1, 1, 1);
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

camera.position.z = 5;

// Audio Analysis Setup
let audioContext, analyser, microphone, dataArray;
let audioReactivity = false;

async function initAudio() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        microphone = audioContext.createMediaStreamSource(stream);
        microphone.connect(analyser);
        audioReactivity = true;
    } catch (error) {
        console.error('Error accessing microphone:', error);
    }
}

// Gyroscope Setup
let gyroEnabled = false;
let gyroImpact = { x: 0, y: 0 };

function handleOrientation(event) {
    if (!gyroEnabled) return;
    
    const x = event.beta * Math.PI / 180;
    const y = event.gamma * Math.PI / 180;
    
    gyroImpact.x = x;
    gyroImpact.y = y;
}

// Idle Animation
function idleAnimation(time) {
    const idleAmplitude = 0.05;
    const idleFrequency = 0.001;
    return Math.sin(time * idleFrequency) * idleAmplitude;
}

// Ferrofluid Movement
let targetPosition = new THREE.Vector3();
function updateFerrofluidPosition(time) {
    const radius = 2;
    const speed = 0.0005;
    targetPosition.x = Math.sin(time * speed) * radius;
    targetPosition.y = Math.cos(time * speed) * radius;
    targetPosition.z = Math.sin(time * speed * 0.5) * radius * 0.5;

    ferrofluid.position.lerp(targetPosition, 0.05);
}

// Animation
function animate() {
    requestAnimationFrame(animate);

    const time = Date.now();
    let audioImpact = 0;
    let totalImpact = 0;

    // Audio reactivity
    if (audioReactivity && analyser) {
        analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        audioImpact = average / 256; // Normalized to 0-1 range
    }

    // Combine idle animation, audio impact, and gyro impact
    totalImpact = idleAnimation(time) + audioImpact * 0.2 + (Math.abs(gyroImpact.x) + Math.abs(gyroImpact.y)) * 0.1;

    // Apply distortion to ferrofluid
    const positions = ferrofluid.geometry.attributes.position.array;
    for (let i = 0; i < positions.length; i += 3) {
        const vertex = new THREE.Vector3(positions[i], positions[i+1], positions[i+2]);
        const distance = vertex.length();
        const amplitude = totalImpact;
        const noise = Math.sin(distance * 10 + time * 0.005) * amplitude;
        vertex.normalize().multiplyScalar(1 + noise);
        positions[i] = vertex.x;
        positions[i+1] = vertex.y;
        positions[i+2] = vertex.z;
    }
    ferrofluid.geometry.attributes.position.needsUpdate = true;

    // Rotate ferrofluid
    ferrofluid.rotation.x += 0.001 + audioImpact * 0.01 + Math.abs(gyroImpact.y) * 0.01;
    ferrofluid.rotation.y += 0.001 + audioImpact * 0.01 + Math.abs(gyroImpact.x) * 0.01;

    // Scale ferrofluid based on total impact
    const scale = 1 + totalImpact * 0.5;
    ferrofluid.scale.set(scale, scale, scale);

    // Move ferrofluid around the page
    updateFerrofluidPosition(time);

    renderer.render(scene, camera);
}

// Event Listeners
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

window.addEventListener('deviceorientation', handleOrientation);

document.querySelector('.cta-button').addEventListener('click', async () => {
    if (!audioContext) {
        await initAudio();
    }
    gyroEnabled = true;
});

animate();