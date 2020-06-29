document.querySelector('.logo').addEventListener('click', function(){
    window.location.replace("http://127.0.0.1:8000/");
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
