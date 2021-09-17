import '../sass/art.sass'

const artwork = document.querySelector('.artwork')
const artworkList = document.querySelector('.artwork-list')
const artworkFullSizeLink = document.querySelector('.artwork-full-size-link')
const footer = document.querySelector('footer')
const linkNext = document.querySelector('.artwork-link-next')
const linkPrevious = document.querySelector('.artwork-link-previous')
const dragThreshold = 75
let currentModal
let dragStartY
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
    currentModal = document.createElement('div')
    currentModal.classList.add('modal-wrapper')
  }
  currentModal.addEventListener('click', () => closeModal())
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
  dragStartY = unifyTouchEvent(event).clientY
}

const endDrag = (event) => {
  const dragStopX = unifyTouchEvent(event).clientX
  const dragStopY = unifyTouchEvent(event).clientY

  if (dragStopY > dragStartY + dragThreshold) {
    return
  }
  if (dragStopY < dragStartY - dragThreshold) {
    return
  }

  if (dragStopX > dragStartX + dragThreshold) {
    navigateToPrevious()
  }
  if (dragStopX < dragStartX - dragThreshold) {
    navigateToNext()
  }
}


artworkFullSizeLink && artworkFullSizeLink.addEventListener('click', event => {
  event.preventDefault()
  openInModal(createImageNode(event.currentTarget))
})
artwork && artwork.addEventListener('touchstart', startDrag, {passive: true})
artwork && artwork.addEventListener('touchend', endDrag, {passive: true})
document.addEventListener('keyup', navigateArtwork)


const startInfiniteScroll = () => {
  if (!artworkList) {
    return;
  }
  const parser = new DOMParser()
  let page = 1

  const appendArtwork = (data) => {
    if (!data) {
      return
    }
    for (const node of parser.parseFromString(data, 'text/html').body.childNodes) {
      artworkList.append(node)
    }
  }

  const refreshObserver = () => {
    observer.unobserve(footer)
    observer.observe(footer)
  }

  const loadMoreArtwork = () => {
    page += 1

    fetch(`async-artworks?page=${page}`).then(
      response => response.text()
    ).then(
      data => appendArtwork(data)
    ).then(
      () => refreshObserver()
    )
  }

  const handleIntersection = (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && page < artworkList.dataset.pageCount) {
        loadMoreArtwork()
      }
    })
  }

  const observer = new IntersectionObserver(handleIntersection, {
    root: null,
    rootMargin: '0px',
    threshold: .1
  })
  observer.observe(footer)
}
startInfiniteScroll()
