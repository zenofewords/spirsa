import '../sass/base.sass'

const mobileMenuToggle = document.getElementById('mobile-nav-toggle')

mobileMenuToggle.addEventListener('click', () => {
  document.body.classList.toggle('scroll-lock')
})
