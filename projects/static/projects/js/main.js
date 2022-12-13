
let global = {
    scroll: 0,
    cardScroll: {
        position: -1,
        height: 3000,
        elementHeight: 0,
        getVariables() {
            const cssMargin = 80
            let dy = window.scrollY - global.cardScroll.position
            let distance = global.cardScroll.height - global.cardScroll.elementHeight - cssMargin
            return {cssMargin, dy, distance}
        }
    },
    carousel: {
        isAnimationInProcess: false,
        animationTime: 300,
        hovered: null
    }
}

function cardHovered(event) {
    if (!global.carousel.isAnimationInProcess) {
        Array.from(document.querySelectorAll('.carousel-images__card')).forEach(x => {
            let target = event.target.closest('.carousel-images__card')
            if (x === target) {
                x.classList.add('is-active')
            } else {
                x.classList.remove('is-active')
            }
        });
        global.carousel.isAnimationInProcess = true
        setTimeout(() => global.carousel.isAnimationInProcess = false, global.carousel.animationTime)
    }
}

function openBurger(event) {
    document.querySelector('.nav-burger-menu').classList.add('is-active');
}

function closeBurger(event) {
    document.querySelector('.nav-burger-menu').classList.remove('is-active');
}

function initializeCardsScrolling() {
    global.scroll = window.scrollY
    document.querySelector('.about-us-scrollwrapper').style.height = `${global.cardScroll.height * 0.9}px`
    let box = document.querySelector('.about-us').getBoundingClientRect()
    global.cardScroll.position = box.top + window.scrollY
    global.cardScroll.elementHeight = box.height
    if (window.scrollY > global.cardScroll.position + global.cardScroll.elementHeight) {
        document.querySelectorAll('.about-us__card').forEach(x => x.style.opacity = '0');
    }
}

window.addEventListener('load', () => {
    /* облака плывут */
    let aboutUsBackgroundPosition = 0;
    setInterval(() => {
        aboutUsBackgroundPosition += 0.02;
        document.querySelector('.about-us').style.backgroundPosition = `${-aboutUsBackgroundPosition}% 0`
    }, 10)

    initializeCardsScrolling()
})

window.addEventListener('resize', () => {
    initializeCardsScrolling()
})

window.addEventListener('scroll', (event) => {
    if (global.cardScroll.position === -1) {
        return
    }
    const {cssMargin, dy, distance} = global.cardScroll.getVariables()
    if (dy > 0 && dy < distance) {
        let y = window.scrollY - global.cardScroll.position;
        document.querySelector('.about-us').style.position = `fixed`
        document.querySelector('.about-us').style.top = `${-y * 0.1}px`
        document.querySelector('.about-us').style.left = '0'
        const progress = y / distance
        const cards = document.querySelectorAll('.about-us__card');
        cards.forEach((x) => {
            let index = +x.getAttribute('data-index') - 1
            let b = (1 - 1 / cards.length) - (index / cards.length) * 0.8;
            let c = 0.001
            let ascend = (((progress - b) / Math.sqrt(c + Math.pow(progress - b, 2))) + 1)
            x.style.top = `${-200 * ascend}px`
            x.style.left = `${-15 * ascend}px`
            x.style.opacity = `${1.5 - ascend}`
            x.style.transform = `rotate(${3 * ascend}deg)`
        })
    } else if (dy <= 0) {
        document.querySelector('.about-us').style.position = `relative`
        document.querySelector('.about-us').style.top = `0px`
    } else if (dy >= distance) {
        document.querySelector('.about-us').style.position = `relative`
        document.querySelector('.about-us').style.top = `${distance * 0.9}px`
    }

})

