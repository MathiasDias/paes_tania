document.querySelector('.logo').addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:8000/");
});

document.querySelector('.qs').addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:8000/quemsomos");
});

if (document.querySelector('#login') != null) {
document.querySelector("#login").addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'flex';
    document.querySelector('.log').style.backgroundColor = 'white';
});
}

document.querySelectorAll(".close").forEach( reg => {
    reg.addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'none';
    document.querySelector('.bg-modal_2').style.display = 'none';
});
});

document.querySelectorAll(".reg").forEach( reg => {
    reg.addEventListener('click', function(){
    document.querySelector('.reg2').style.background = 'white';
    document.querySelector('.bg-modal').style.display = 'none';
    document.querySelector('.bg-modal_2').style.display = 'flex';
});
});

document.querySelectorAll(".log").forEach( log => {
    log.addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'flex';
    document.querySelector('.bg-modal_2').style.display = 'none';
});
});

var slideIndex = 1;
showSlides(slideIndex);

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("foto-slider");
  var dots = document.getElementsByClassName("thumb_fotos");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}
