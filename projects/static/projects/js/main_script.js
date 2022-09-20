document.querySelectorAll('body *').forEach(x => {
    x.style.transform = `rotate(${-1 + Math.random() * 2}deg)`
})

function showEnru() {
    alert('Если бы это был настоящий сайт, то весь текст на сайте поменял бы локализацию')
}

function showAbout() {
    document.querySelector('.about-us').classList.toggle('is-active')
}

let mousetimeoutlastin = new Date()
let mousetimeoutlastout = new Date()

function aboutUsMousein() {
    mousetimeoutlastin = new Date()
}

function aboutUsMouseout() {
    mousetimeoutlastout = new Date()
    setTimeout(() => {
        if (mousetimeoutlastout > mousetimeoutlastin) {
            document.querySelector('.about-us').classList.remove('is-active')
        }
    }, 1500)
}

function downloaded() {
    alert('Представь, что скачалось')
}