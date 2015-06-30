function projectExpander() {
    var expander = document.getElementById("menubarProj")
    if (expander.style.display == "none") {
        expander.style.display = "block"
        document.getElementById("projExpander").innerHTML = "-"
    } else {
        expander.style.display = "none"
        document.getElementById("projExpander").innerHTML = "+"
    }
}