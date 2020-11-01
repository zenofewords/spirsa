import '../sass/art.sass'

const artwork = document.querySelector('.artwork')
const artworkFullSizeLink = document.querySelector('.artwork-full-size-link')
const linkNext = document.querySelector('.artwork-link-next')
const linkPrevious = document.querySelector('.artwork-link-previous')
const dragThreshold = 100
let currentModal
let dragStartX

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
  dragStartX = unifyTouchEvent(event).clientX
}

const endDrag = (event) => {
  let dragStopX = unifyTouchEvent(event).clientX
  dragStopX = dragStopX > 0 ? dragStopX + dragThreshold : dragStopX - dragThreshold
  dragStopX > dragStartX ? navigateToPrevious() : navigateToNext()
}


artworkFullSizeLink.addEventListener('click', event => {
  event.preventDefault()
  openInModal(createImageNode(event.currentTarget))
})
document.addEventListener('keyup', navigateArtwork)
artwork.addEventListener('touchstart', startDrag)
artwork.addEventListener('touchend', endDrag)
