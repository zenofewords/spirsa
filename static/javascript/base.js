import '../sass/base.sass'

const mobileMenuToggle = document.getElementById('mobile-menu-toggle')

mobileMenuToggle.addEventListener('click', event => {
  document.body.classList.toggle('scroll-lock')
})
