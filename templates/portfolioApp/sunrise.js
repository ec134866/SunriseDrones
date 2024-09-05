import * as THREE from 'three';
import WebGL from 'three/addons/capabilities/WebGL.js';
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GUI } from 'three/addons/libs/lil-gui.module.min.js';

let camera, scene, renderer, loader, object;

const params = {
    asset: 'resized'
};

const assets = [
    'Master',
    'resized'
];


const assetURLs = {
    'Master': './public/Master.fbx',
    'resized': 'https://drive.google.com/uc?id=1U3Tp6qWRxJjEubSteFu9Tti2pAcPHYpy&export=download'
};




init();

function init() {
    const container = document.createElement('div');
    document.body.appendChild(container);

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 200000);
    camera.position.set(10, 40, 60);

    scene = new THREE.Scene();

    const light = new THREE.AmbientLight(0x404040, 100);
    scene.add(light);

    loader = new FBXLoader();
    loadAsset(params.asset);

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setAnimationLoop(animate);
    container.appendChild(renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = false;
    controls.enablePan = false;
    controls.minDistance = 0;
    controls.maxDistance = 100000;
    controls.minPolarAngle = 0.25;
    controls.maxPolarAngle = 1.8;
    controls.autoRotate = false;
    controls.target = new THREE.Vector3(0, 1, 0);
    controls.update();

    window.addEventListener('resize', onWindowResize);

    const gui = new GUI();
    gui.add(params, 'asset', assets).onChange((value) => {
        loadAsset(value);
    });
}

function loadAsset(asset) {
    const url = assetURLs[asset]; // Get the URL from the mapping
    if (!url) {
        console.error('Asset URL not found');
        return;
    }

    loader.load(url, (group) => {
        if (object) scene.remove(object);

        object = group;
        scene.add(object);
    }, undefined, (error) => {
        console.error(error);
    });
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    renderer.render(scene, camera);
}
