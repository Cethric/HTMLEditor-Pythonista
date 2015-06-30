var list = document.getElementById("project_list");
var posts = document.getElementById('posts');
document.onclick = function(event){
    var list_parent = false;
    var more_parent = false;
    for(var node = event.target; node != document.body; node = node.parentNode)
    {
        if(node.id == 'projects_item'){
            list_parent = true;
            break;
        } else if (node.id == 'more_menu') {
            more_parent = true;
        }
    }
    if(list_parent)
        list_handle();
    else
        list.style.display = 'none';
    if(more_parent)
        more_menu();
    else
        posts.style.right = "-50em";
}
document.onkeydown = function(event) {
    if (event.keyCode == 27) {
        list.style.display = 'none';
        posts.style.right = "-50em";
    }
}

function list_handle() {
    if (list.style.display=='none') {
        list.style.display = 'block';
    } else {
        list.style.display = 'none';
    }
}

function more_menu() {
    if (posts.style.right=='-50em') {
        posts.style.right = "0";
    } else {
        posts.style.right = "-50em";
    }
    }