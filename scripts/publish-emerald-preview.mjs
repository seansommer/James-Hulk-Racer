import {cp,access} from 'node:fs/promises';
// Keep the existing game at the root and publish the illustrated practice game beside it.
await access('dist-preview/preview/index.html');
await cp('dist-preview/preview','dist/emerald',{recursive:true});
await cp('dist-preview/assets','dist/assets',{recursive:true});
console.log('Published Emerald practice game at /James-Hulk-Racer/emerald/.');
