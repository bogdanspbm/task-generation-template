document.getElementById('file-input').addEventListener('change', handleFileSelect);
document.getElementById('delete-button').addEventListener('click', handleDeleteTasks);
document.getElementById('send-button').addEventListener('click', handleSendTasks);


let tasks = [];
let canSend = false;

const difficultyMap = {"easy": "Легкая", "medium": "Среднея", "hard": "Сложная"}

function handleDeleteTasks(event) {
    tasks = [];
    const taskContainer = document.querySelector('.task-container');
    taskContainer.classList.add("hidden");
    showImportButton();
    updateFields({});
}

function handleSendTasks(event) {

}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            try {
                tasks = JSON.parse(e.target.result);
                updateFields(tasks[0]);  // Проверяем и обновляем поля для первой задачи
                displayTask(tasks[0]);  // Отображаем первую задачу
                showSendButton();
            } catch (error) {
                console.error('Ошибка при разборе JSON:', error);
            }
        };
        reader.readAsText(file);
    }
}

function showSendButton() {
    const multiButton = document.getElementById("multi-button");
    const importButton = document.getElementById("import-button");
    const sendButton = document.getElementById("send-button");

    importButton.style.display = 'none';
    multiButton.style.display = 'flex';

    if (canSend) {
        sendButton.removeAttribute('disabled');
    } else {
        sendButton.setAttribute("disabled", "true");
    }
}

function showImportButton() {
    const sendButton = document.getElementById("multi-button");
    const importButton = document.getElementById("import-button");

    importButton.style.display = 'flex';
    sendButton.style.display = 'none';
    canSend = false;
}


function updateField(fieldId, fieldValue, isValid, errorMessage = '') {
    const fieldElement = document.getElementById(fieldId).querySelector('img');
    const tooltipElement = document.getElementById(fieldId).querySelector('.tooltip');

    if (!isValid) {
        fieldElement.classList.remove('success-load-field', 'empty-load-field');
        fieldElement.classList.add('empty-load-field');
        tooltipElement.style.visibility = null;
        tooltipElement.textContent = errorMessage || 'Неверный формат поля';
        canSend = false;
    } else {
        fieldElement.classList.remove('empty-load-field');
        fieldElement.classList.add('success-load-field');
        tooltipElement.style.visibility = 'hidden';
        tooltipElement.textContent = ''; // Очистка текста ошибки
    }
}

function updateFields(task) {
    canSend = true;
    updateField('uid', task.uid, validateUid(task.uid), 'UID должен содержать 10 символов (заглавные буквы и цифры)');
    updateField('task_num', task.task_num, task.task_num !== undefined && task.task_num !== null, 'Номер задачи обязателен');
    updateField('task_subject', task.task_subject, task.task_subject !== undefined && task.task_subject !== null, 'Предмет задачи обязателен');
    updateField('task_types', task.task_types, task.task_types !== undefined && task.task_types.length > 0, 'Тип задачи обязателен');
    updateField('fipi_uid', task.fipi_uid, task.fipi_uid !== undefined && task.fipi_uid !== null, 'FIPI UID обязателен');
    updateField('task_text', task.task_text, task.task_text !== undefined && task.task_text !== null, 'Текст задачи обязателен');
    updateField('task_html', task.task_html, task.task_html !== undefined && task.task_html !== null, 'HTML задачи обязателен');
    updateField('task_answer', task.task_answer, task.task_answer !== undefined && task.task_answer !== null, 'Ответ задачи обязателен');
    updateField('task_solution', task.task_solution, task.task_solution !== undefined && task.task_solution !== null, 'Решение задачи обязательно');
    updateField('task_hints', task.task_hints, Array.isArray(task.task_hints) && task.task_hints.length > 0, 'Должна быть хотя бы одна подсказка');
    updateField('answer_type', task.answer_type, task.answer_type !== undefined && task.answer_type !== null, 'Тип ответа обязателен');
    updateField('task_group_key', task.task_group_key, task.task_group_key !== undefined && task.task_group_key !== null, 'Код группы обязателен');
    updateField('task_group_label', task.task_group_label, task.task_group_label !== undefined && task.task_group_label !== null, 'Имя группы обязательно');
    updateField('task_images', task.task_images, validateTaskImages(task.task_images), 'Картинки должны быть массивом строк или null');
    updateField('task_images_svg', task.task_images_svg, validateTaskImages(task.task_images_svg), 'SVG картинки должны быть массивом строк или null');
}


function validateUid(uid) {
    return /^[A-Z0-9]{10}$/.test(uid);
}

function validateTaskImages(images) {
    return !images || (Array.isArray(images) && (images.every(img => typeof img === 'string') || images.length === 0));
}

function displayTask(task) {
    const taskContainer = document.querySelector('.task-container');
    const taskContent = document.querySelector('.task-content-container');
    const taskTitle = document.querySelector('.title-container h3');
    const taskDescription = document.querySelector('.title-container p');
    const taskDifficulty = document.querySelector('.difficulty');
    const taskDuration = document.querySelector('.duration');

    document.taskJSON = task;

    // Обновляем контент задачи
    taskTitle.textContent = task.uid;
    taskDescription.textContent = task.task_subject;
    taskDifficulty.textContent = validateDifficulty(task.difficulty) ? difficultyMap[task.difficulty] : 'неизвестно';
    taskDuration.textContent = "15 мин";  // Здесь вы можете указать реальное значение из задачи, если оно есть

    // Вставляем HTML задачи
    handleShowDesc();

    // Отображаем контейнер задачи, убирая класс "hidden"
    taskContainer.classList.remove('hidden');
}

function validateDifficulty(difficulty) {
    return ['easy', 'medium', 'hard'].includes(difficulty);
}
