const mobileMenuToggle = document.getElementById("mobile-nav-toggle");

mobileMenuToggle?.addEventListener("click", () => {
  document.body.classList.toggle("scroll-lock");
});

const artwork = document.querySelector<HTMLElement>(".artwork");
const artworkList = document.querySelector<HTMLElement>(".artwork-list");
const artworkFullSizeLink = document.querySelector<HTMLAnchorElement>(
  ".artwork-full-size-link",
);
const footer = document.querySelector<HTMLElement>("footer");
const linkNext = document.querySelector<HTMLAnchorElement>(
  ".artwork-link-next",
);
const linkPrevious = document.querySelector<HTMLAnchorElement>(
  ".artwork-link-previous",
);
const dragThreshold = 75;
let currentModal: HTMLDivElement | null = null;
let dragStartX = 0;
let dragStartY = 0;

const createImageNode = (element: HTMLAnchorElement): HTMLImageElement => {
  const imageNode = document.createElement("img");
  imageNode.setAttribute("class", "artwork-full-size-image");
  imageNode.setAttribute("src", element.href);
  imageNode.setAttribute("alt", element.ariaLabel || "");
  return imageNode;
};

const openInModal = (element: HTMLImageElement): void => {
  if (!currentModal) {
    currentModal = document.createElement("div");
    currentModal.classList.add("modal-wrapper");
  }
  currentModal.addEventListener("click", () => closeModal());
  currentModal.appendChild(element);
  document.body.appendChild(currentModal);
  document.body.classList.add("scroll-lock");
  document.addEventListener("keyup", keyupCloseModal);
};

const closeModal = (): void => {
  if (!currentModal) return;
  currentModal.innerHTML = "";
  currentModal.remove();
  document.body.classList.remove("scroll-lock");
  document.removeEventListener("keyup", keyupCloseModal);
};

const keyupCloseModal = (event: KeyboardEvent): void => {
  if (currentModal && event.key === "Escape") {
    closeModal();
  }
};

const navigateToPrevious = (): void => {
  if (linkPrevious) {
    window.location.href = linkPrevious.href;
  }
};

const navigateToNext = (): void => {
  if (linkNext) {
    window.location.href = linkNext.href;
  }
};

const navigateArtwork = (event: KeyboardEvent): void => {
  if (event.key === "ArrowLeft") {
    navigateToPrevious();
  }
  if (event.key === "ArrowRight") {
    navigateToNext();
  }
};

const unifyTouchEvent = (event: TouchEvent): Touch | TouchEvent => {
  return event.changedTouches ? event.changedTouches[0] : event;
};

const startDrag = (event: TouchEvent): void => {
  const touch = unifyTouchEvent(event);
  dragStartX = touch.clientX;
  dragStartY = touch.clientY;
};

const endDrag = (event: TouchEvent): void => {
  const touch = unifyTouchEvent(event);
  const dragStopX = touch.clientX;
  const dragStopY = touch.clientY;

  if (dragStopY > dragStartY + dragThreshold) return;
  if (dragStopY < dragStartY - dragThreshold) return;

  if (dragStopX > dragStartX + dragThreshold) {
    navigateToPrevious();
  }
  if (dragStopX < dragStartX - dragThreshold) {
    navigateToNext();
  }
};

artworkFullSizeLink?.addEventListener("click", (event: Event) => {
  event.preventDefault();
  openInModal(createImageNode(event.currentTarget as HTMLAnchorElement));
});
artwork?.addEventListener("touchstart", startDrag, { passive: true });
artwork?.addEventListener("touchend", endDrag, { passive: true });
document.addEventListener("keyup", navigateArtwork);

const startInfiniteScroll = (): void => {
  if (!artworkList || !footer) return;

  const list = artworkList;
  const footerEl = footer;
  const parser = new DOMParser();
  let page = 1;

  const appendArtwork = (data: string): void => {
    if (!data) return;
    for (const node of parser.parseFromString(data, "text/html").body
      .childNodes) {
      list.append(node);
    }
  };

  const refreshObserver = (): void => {
    observer.unobserve(footerEl);
    observer.observe(footerEl);
  };

  const loadMoreArtwork = (): void => {
    page += 1;
    let path = window.location.pathname;
    path = path !== "/" ? path : "featured";

    fetch(`${path}/async-artworks?page=${page}&path=${path}`)
      .then((response) => response.text())
      .then((data) => appendArtwork(data))
      .then(() => refreshObserver());
  };

  const handleIntersection = (entries: IntersectionObserverEntry[]): void => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && page < Number(list.dataset.pageCount)) {
        loadMoreArtwork();
      }
    });
  };

  const observer = new IntersectionObserver(handleIntersection, {
    root: null,
    rootMargin: "500px",
    threshold: 0.1,
  });
  observer.observe(footerEl);
};

startInfiniteScroll();
