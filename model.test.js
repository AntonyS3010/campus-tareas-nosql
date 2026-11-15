import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeTask } from './public/model.js';
test('normaliza espacios sin cambiar el contenido de la tarea', () => {
  assert.deepEqual(normalizeTask('  Leer capítulo 2  ', ' BD II '), {title:'Leer capítulo 2', course:'BD II'});
});
test('rechaza nombres vacíos y valores que exceden los límites de Firestore', () => {
  for (const [title, course] of [[' ', 'BD'], ['Leer', ' '], ['x'.repeat(121), 'BD'], ['Leer', 'x'.repeat(61)]]) {
    assert.throws(() => normalizeTask(title, course));
  }
  assert.equal(normalizeTask('x'.repeat(120), 'y'.repeat(60)).title.length, 120);
});
