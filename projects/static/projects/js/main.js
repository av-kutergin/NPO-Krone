
let global = {
    scroll: 0,
    cardScroll: {
        position: -1,
        height: 3000,
        windowHeight: 800,
        elementHeight: 0,
        getVariables() {
            const cssMargin = 80
            let dy = window.scrollY - global.cardScroll.position
            let distance = global.cardScroll.height - global.cardScroll.elementHeight - cssMargin
            let condencedCorrection = global.cardScroll.windowHeight > 500 ? 0 : -70;
            return {cssMargin, dy, distance, condencedCorrection}
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
    global.cardScroll = {...global.cardScroll, ...{
        position: -1,
        height: 3000,
        windowHeight: 800,
        elementHeight: 0,
    }}
    global.cardScroll.windowHeight = window.innerHeight * 1.1;
    global.scroll = window.scrollY
    document.querySelector('.about-us-scrollwrapper').style.height = `${global.cardScroll.height * 0.9}px`
    document.querySelector('.about-us').style.height = `${global.cardScroll.windowHeight}px`
    
    if (global.cardScroll.windowHeight < 500) {
        document.querySelector('.about-us').classList.add('is-condenced')
    } else {
        document.querySelector('.about-us').classList.remove('is-condenced')
    }

    let aspectRatio = document.querySelector('.about-us .container').getBoundingClientRect().width / window.innerHeight
    console.log(aspectRatio)
    let columnsCount = aspectRatio > 1.7 ? 3 : aspectRatio < 1 ? 1 : 2;
    document.querySelector('.about-us').setAttribute('data-columns', columnsCount)

    let maxCardHeight = Array.from(document.querySelectorAll('.about-us__card')).reduce((a, c) => {
        let height = c.getBoundingClientRect().height
        return height > a ? height : a
    }, 0)
    document.querySelectorAll('.about-us__card').forEach(x => x.style.height = `${maxCardHeight}px`)

    let box1 = document.querySelector('.about-us-scrollwrapper').getBoundingClientRect()
    let box2 = document.querySelector('.about-us').getBoundingClientRect()
    global.cardScroll.position = box1.top + window.scrollY
    global.cardScroll.elementHeight = box2.height
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

window.addEventListener('scroll', (event) => {
    if (global.cardScroll.position === -1) {
        return
    }
    let {cssMargin, dy, distance, condencedCorrection} = global.cardScroll.getVariables()
    condencedCorrection = 0;
    if (dy > 0 && dy < distance) {
        let y = window.scrollY - global.cardScroll.position;
        const progress = y / distance
        const cards = document.querySelectorAll('.about-us__card');
        document.querySelector('.about-us').style.position = `fixed`
        document.querySelector('.about-us').style.top = `${-y * 0.1}px`
        document.querySelector('.about-us').style.left = '0'
        document.querySelector('.about-us-scrollwrapper').style.background = `rgba(79, 75, 105, ${(1 - progress) * 10})`
        cards.forEach((x) => {
            let index = +x.getAttribute('data-index') - 1
            let b = (1 - 1 / cards.length) - (index / cards.length) * 0.8;
            let c = 0.001
            let ascend = (((progress - b) / Math.sqrt(c + Math.pow(progress - b, 2))) + 1)
            x.style.top = `${-300 * ascend + condencedCorrection + y * 0.08}px`
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

window.addEventListener('resize', (event) => {
    initializeCardsScrolling()
})