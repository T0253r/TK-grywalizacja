// to jest do podświetlenia wybranego panelu

const button_dict = {
    "home": "/",
    "tree": "/tree",
    "rank": "/ranking",
    "user": "/dashboard"
}

const url = window.location.href

document.querySelectorAll('button').forEach(button => {
    if (url.endsWith(button_dict[button.id])) {
        button.classList.add("bg-gray-300")
    }
})