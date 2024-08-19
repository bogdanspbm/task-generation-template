const scaleButton = document.getElementById("scale-image-button");

if(scaleButton){
    scaleButton.addEventListener("click", scaleHandler);
}

function scaleHandler() {
    const imageContainer = document.getElementById("task-image-container");
    if(imageContainer.classList.contains("expanded")){
        imageContainer.classList.remove("expanded");
        imageContainer.style.maxWidth = "";
        imageContainer.style.width = "";
        imageContainer.style.minWidth = "";
    } else {
        imageContainer.classList.add("expanded");
        imageContainer.style.maxWidth = "600px";
        imageContainer.style.minWidth = "600px";
        imageContainer.style.width = "600px";
    }
}
