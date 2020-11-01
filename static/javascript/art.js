import '../sass/art.sass'

const artworkFullSizeLink = document.querySelector('.artwork-full-size-link')
const linkPrevious = document.querySelector('.artwork-link-previous')
const linkNext = document.querySelector('.artwork-link-next')
let currentModal
let dragX


const createImageNode = (element) => {
  const imageNode = document.createElement('img')
  imageNode.setAttribute('class', 'artwork-full-size-image')
  imageNode.setAttribute('src', element.href)
  imageNode.setAttribute('alt', element.ariaLabel)
  return imageNode
}

const openInModal = (element) => {
  if (!currentModal) {
    currentModal = document.createElement('modal')
    currentModal.classList.add('modal-wrapper')
  }
  currentModal.addEventListener('click', event => closeModal())
  currentModal.appendChild(element)
  document.body.appendChild(currentModal)
  document.body.classList.add('scroll-lock')
  document.addEventListener('keyup', keyupCloseModal)
}

const closeModal = () => {
  currentModal.innerHTML = ''
  currentModal.remove()
  document.body.classList.remove('scroll-lock')
  document.removeEventListener('keyup', keyupCloseModal)
}

const keyupCloseModal = (event) => {
  if (currentModal && event.key === 'Escape') {
    closeModal()
  }
}

const navigateToPrevious = () => {
  if (linkPrevious) {
    window.location.href = linkPrevious.href
  }
}

const navigateToNext = () => {
  if (linkNext) {
    window.location.href = linkNext.href
  }
}

const navigateArtwork = (event) => {
  if (event.key === 'ArrowLeft') {
    navigateToPrevious()
  }
  if (event.key === 'ArrowRight') {
    navigateToNext()
  }
}

const unifyTouchEvent = (event) => {
  return event.changedTouches ? event.changedTouches[0] : event
}

const startDrag = (event) => {
  dragX = unifyTouchEvent(event).clientX
}

const endDrag = (event) => {
  unifyTouchEvent(event).clientX > dragX ? navigateToPrevious() : navigateToNext()
}


artworkFullSizeLink.addEventListener('click', event => {
  event.preventDefault()
  openInModal(createImageNode(event.currentTarget))
})
document.addEventListener('keyup', navigateArtwork)
document.addEventListener('touchstart', startDrag)
document.addEventListener('touchend', endDrag)
