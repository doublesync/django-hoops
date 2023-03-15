copyButtons = document.getElementsByClassName("copyJSON");

function clipboard(clicked_id) {
    // Get the closest element with the class "file"
    let btn = document.getElementById(clicked_id);
    let file = document.getElementById(`json_${clicked_id}`);
    // Copy the file to the clipboard
    navigator.clipboard.writeText(file.innerText);
    btn.innerText = "Copied!";
    btn.classList.remove("btn-primary");
    btn.classList.add("btn-success");
}