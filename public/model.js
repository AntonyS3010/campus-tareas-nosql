export function normalizeTask(title, course) {
  const task = { title: title.trim(), course: course.trim() };
  if (!task.title || task.title.length > 120) throw new Error('Escribe una tarea de entre 1 y 120 caracteres.');
  if (!task.course || task.course.length > 60) throw new Error('Escribe un curso de entre 1 y 60 caracteres.');
  return task;
}
