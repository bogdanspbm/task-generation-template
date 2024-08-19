const descButton = document.getElementById('task-description');
const commentButton = document.getElementById('task-comments');
const hintsButton = document.getElementById('task-hints');
const solutionButton = document.getElementById('task-solutions');

descButton.addEventListener("click", () => handleShowDesc());
hintsButton.addEventListener("click", () => handleShowHints());
solutionButton.addEventListener("click", () => handleShowSolutions());

function deselectButtons(){
    descButton.classList.remove("selected");
    commentButton.classList.remove("selected");
    hintsButton.classList.remove("selected");
    solutionButton.classList.remove("selected");
}

function getAndClearTaskFragment(){
    const taskFragment = document.getElementById("task-fragment");
    taskFragment.replaceChildren([]);
    return taskFragment;
}

function handleShowSolutions() {
    if (!document.taskJSON) {
        return;
    }

    deselectButtons();
    solutionButton.classList.add("selected");
    const fragment = getAndClearTaskFragment();

    const container = document.createElement("div");
    container.classList.add("task-hint-item");
    container.innerHTML = document.taskJSON['task_solution'];
    fragment.appendChild(container);


    const answerContainer = document.getElementById('answer-input-container');
    answerContainer.style.display = 'none';
}

function getImageElement(task = {}) {


    if(!task['task_images_svg'] || task['task_images_svg'].length < 1){
        return null;
    }

    const imageContainer = document.createElement("div");
    imageContainer.classList.add("task-image-container");
    imageContainer.id = "task-image-container";

    const imageElement = document.createElement("div");
    imageElement.classList = "svg-image";
    imageElement.innerHTML = task['task_images_svg'][0];
    const svgImage = imageElement.children[0];
    console.log(svgImage);

    const scaleButton = document.createElement("div");
    scaleButton.id = "scale-image-button";
    scaleButton.classList.add("scale-button", "item-shadow");
    scaleButton.innerHTML = '<img src="./resources/icons/ic_search_24x24.svg">';
    scaleButton.onclick = scaleHandler;

    imageContainer.appendChild(imageElement)
    imageContainer.appendChild(scaleButton);
    return imageContainer;
}

function handleShowHints() {
    if (!document.taskJSON) {
        return;
    }

    deselectButtons();
    hintsButton.classList.add("selected");
    const fragment = getAndClearTaskFragment();

    for(let i = 0; i < document.taskJSON['task_hints'].length; i++){
        const hint = document.taskJSON['task_hints'][i];
        const container = document.createElement("div");
        container.classList.add("task-hint-item");
        container.innerHTML = hint;
        fragment.appendChild(container);
    }


    const answerContainer = document.getElementById('answer-input-container');
    answerContainer.style.display = 'none';
}

function handleShowDesc() {
    if (!document.taskJSON) {
        return;
    }

    deselectButtons();
    descButton.classList.add("selected");
    const fragment = getAndClearTaskFragment();

    const container = document.createElement("div");
    container.classList.add("task-content-container");
    container.innerHTML = document.taskJSON['task_html'];


    const image = getImageElement(document.taskJSON);
    if(image) {
        container.appendChild(image);
    }
    fragment.appendChild(container);


    const answerContainer = document.getElementById('answer-input-container');
    answerContainer.style.display = 'flex';
}