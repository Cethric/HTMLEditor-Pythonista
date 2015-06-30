function project_menu() {
    var list = document.getElementById("project_list");
    if (list.style.display=='none') {
        list.style.display = 'block';
    } else {
        list.style.display = 'none';
    }
}

function more_menu() {
    var list = document.getElementById('posts');
    if (list.style.right=='-50em') {
        list.style.right = "0";
    } else {
        list.style.right = "-50em";
    }
}