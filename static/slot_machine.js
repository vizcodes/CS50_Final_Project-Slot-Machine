
document.addEventListener('DOMContentLoaded', function() {
  var dance = document.getElementById('spin');
  
  function replaceWithRandomEmoji(element) {
    const randomIndex = Math.floor(Math.random() * emojis.length);
    element.textContent = emojis[randomIndex];
  }


  function popper() {
    // var confetti = window.confetti;
    confetti({
      particleCount: 150,
      spread: 60
    });
  };



  let emojis = ['🍌','🍎','🍒','💲','🔥','💀'];
  const updateIntervalInSeconds = 0.1;
  var audio2 = document.getElementById('audio2');
  var audio3 = document.getElementById('audio3');

  audio3.volume = 0.1;
  
  function sounditboy() {
      audio2.play();
      audio3.play();
  }

  var box1 = document.getElementById('box1');
  var box2 = document.getElementById('box2');
  var box3 = document.getElementById('box3');


  function unpress() {
    dance.classList.remove('pressed');
  }

  function playSound() {
    dance.classList.add('pressed');
    box1.classList.add('filter')
    box2.classList.add('filter')
    box3.classList.add('filter')
    var delay = 200;
    setTimeout(unpress, delay);
  }

  

  dance.addEventListener('click', function(event) {
    playSound();
    sounditboy();
    popper();

          // Initial replacement
    setInterval(function () {
      replaceWithRandomEmoji(box1);
      replaceWithRandomEmoji(box2);
      replaceWithRandomEmoji(box3);
          }, updateIntervalInSeconds * 500);
  });

  var slider = document.getElementById("myRange");
  var output = document.getElementById("demo");
  output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
  slider.oninput = function() {
    output.innerHTML = this.value;
  }
});

