function scrollCarousel(direction) {
    const track = document.querySelector('.carousel-track');
    const scrollAmount = 300; // Ancho de una tarjeta
    
    if (direction === 'left') {
      track.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    } else {
      track.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    }
  }
