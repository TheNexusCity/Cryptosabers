/* Loading a gltf file, combining the meshes, and then exporting the combined mesh to a new gltf file. */
import * as THREE from 'three';

import { GLTFExporter } from './GLTFExporter.js';

import fs from 'fs';
import { combine } from './mesh-combination.js';

import { loadGltf } from './node-three-gltf.js';

import { Blob, FileReader } from 'vblob';

import URL from "url";

global = {}
global.THREE = THREE;
global.window = (global);
(global).Blob = Blob; // working
(global).FileReader = FileReader;
global.URL = URL;

const atlasSize = 4096;

process.on('uncaughtException', function (exception) {
    console.log(exception); // to see your exception details in the console
    // if you are on production, maybe you can send the exception details to your
    // email as well ?
});


const inputPath = process.argv[2] ?? './input.glb';
const outputPath = process.argv[3] ?? './output.glb';

export default (async () => {
    try {
        const exporter = new GLTFExporter();
        const model = await loadGltf(inputPath);

        const combinedAvatar = await combine({ avatar: model.scene, atlasSize });
        exporter.parse(combinedAvatar, (gltf) => { fs.writeFileSync(outputPath, Buffer.from(gltf)); }, { binary: true });
    } catch (error) {
        console.log('error', error);
    }
})();
