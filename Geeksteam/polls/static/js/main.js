// navbar style when scrolling

window.addEventListener('scroll', () => {
    document.querySelector('nav').classList.toggle('window-scroll', window.scrollY > 100)
})


// show/hide nav menu
const menu = document.querySelector(".nav__menu");
const menuBtn = document.querySelector("#open-menu-btn");
const closeBtn = document.querySelector("#close-menu-btn");

menuBtn.addEventListener('click', () => {
    menu.style.display = 'flex';
    closeBtn.style.display = 'inline-block';
    menuBtn.style.display = 'none';
})

// close nav menu
const closeNav = () => {
    menu.style.display = 'none';
    closeBtn.style.display = 'none';
    menuBtn.style.display = 'inline-block';
}
closeBtn.addEventListener('click', closeNav)


//display message
const textarea = document.querySelector('.chatbox-message-input')
const chatboxForm = document.querySelector('.chatbox-message-form')


textarea.addEventListener('input', function () {
    let line = textarea.value.split('\n').length
    if (textarea.rows < 6 || line < 6) {
        textarea.rows = line
    }
    if (textarea.rows > 1) {
        chatboxForm.style.alignItems = 'flex-end'
    }
    else {
        chatboxForm.style.alignItems = 'center'

    }
})

