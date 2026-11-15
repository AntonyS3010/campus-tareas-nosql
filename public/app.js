import { normalizeTask } from './model.js';

const $ = id => document.getElementById(id);
let tasks = [], editing = null, collectionRef, db, api, busy = false;
const status = message => { $('status').textContent = message; };
function reset() {
  editing = null; $('task-form').reset(); $('save').textContent = 'Agregar tarea';
  $('form-title').textContent = 'Nueva tarea'; $('cancel').hidden = true;
}
async function mutate(operation) {
  if (busy) return;
  busy = true; $('fields').disabled = true; render();
  try { await operation(); status('Cambios guardados en Firestore.'); }
  catch (error) { console.error(error); status('No se pudo guardar. Comprueba tu conexión y vuelve a intentarlo.'); }
  finally { busy = false; $('fields').disabled = false; render(); }
}
function render() {
  $('list').replaceChildren();
  const visible = tasks.filter(t => $('filter').value === 'all' || t.done === ($('filter').value === 'done'));
  $('count').textContent = `${tasks.filter(t => !t.done).length} pendientes · ${tasks.length} en total`;
  $('empty').hidden = visible.length > 0;
  for (const task of visible) {
    const item = document.createElement('li'); item.classList.toggle('done', task.done);
    const checkbox = document.createElement('input'); checkbox.type = 'checkbox'; checkbox.checked = task.done;
    checkbox.disabled = busy; checkbox.setAttribute('aria-label', `Completar: ${task.title}`);
    checkbox.addEventListener('change', () => mutate(() => api.updateDoc(api.doc(collectionRef, task.id), {done: checkbox.checked})));
    const copy = document.createElement('div'); copy.className = 'task-copy';
    const title = document.createElement('strong'); title.textContent = task.title;
    const course = document.createElement('small'); course.textContent = task.course; copy.append(title, course);
    const actions = document.createElement('div'); actions.className = 'actions';
    for (const [label, callback] of [
      ['Editar', () => { editing = task.id; $('title').value = task.title; $('course').value = task.course; $('save').textContent = 'Guardar cambios'; $('form-title').textContent = 'Editar tarea'; $('cancel').hidden = false; $('title').focus(); }],
      ['Eliminar', () => { if (confirm(`¿Eliminar «${task.title}»?`)) mutate(async () => { await api.deleteDoc(api.doc(collectionRef, task.id)); if (editing === task.id) reset(); }); }]
    ]) {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = label; button.disabled = busy;
      button.addEventListener('click', callback); actions.append(button);
    }
    item.append(checkbox, copy, actions); $('list').append(item);
  }
}
$('cancel').addEventListener('click', reset);
$('filter').addEventListener('change', render);
$('task-form').addEventListener('submit', event => {
  event.preventDefault();
  if (!collectionRef || busy) return;
  let data;
  try { data = normalizeTask($('title').value, $('course').value); }
  catch (error) { status(error.message); return; }
  mutate(async () => {
    if (editing) await api.updateDoc(api.doc(collectionRef, editing), data);
    else await api.addDoc(collectionRef, {...data, done: false, createdAt: api.serverTimestamp()});
    reset();
  });
});
async function start() {
  try {
    // Firebase Hosting proporciona la configuración del proyecto que aloja esta app.
    const response = await fetch('/__/firebase/init.json');
    if (!response.ok) throw new Error('Firebase Hosting no está configurado.');
    const config = await response.json();
    const [appModule, authModule, firestoreModule] = await Promise.all([
      import('https://www.gstatic.com/firebasejs/13.3.0/firebase-app.js'),
      import('https://www.gstatic.com/firebasejs/13.3.0/firebase-auth.js'),
      import('https://www.gstatic.com/firebasejs/13.3.0/firebase-firestore.js')
    ]);
    api = firestoreModule;
    const app = appModule.initializeApp(config);
    const auth = authModule.getAuth(app); db = api.getFirestore(app);
    await authModule.setPersistence(auth, authModule.browserLocalPersistence);
    await auth.authStateReady();
    const credential = auth.currentUser ? {user: auth.currentUser} : await authModule.signInAnonymously(auth);
    collectionRef = api.collection(db, 'users', credential.user.uid, 'tasks');
    api.onSnapshot(api.query(collectionRef, api.orderBy('createdAt', 'desc')), snapshot => {
      tasks = snapshot.docs.map(document => ({...document.data(), id: document.id}));
      $('fields').disabled = busy; render(); status('Tu espacio está conectado.');
    }, error => { console.error(error); $('fields').disabled = true; status('No se pudieron leer las tareas. Revisa la conexión y los permisos de Firestore.'); });
  } catch (error) {
    console.error(error); status('No se pudo conectar. Revisa la configuración de Firebase Hosting, Firestore y la autenticación anónima.');
  }
}
start();
