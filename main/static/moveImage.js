//function leftArrowPressed() {
//            var element = document.getElementById("moving");
//            element.style.left = parseInt(element.style.left) - 5 + 'px';
//            }
//
//            function rightArrowPressed() {
//            var element = document.getElementById("moving");
//            element.style.left = parseInt(element.style.left) + 5 + 'px';
//
//            }
//
//            function upArrowPressed() {
//            var element = document.getElementById("moving");
//            element.style.top = parseInt(element.style.top) - 5 + 'px';
//            }
//
//            function downArrowPressed() {
//            var element = document.getElementById("moving");
//            element.style.top = parseInt(element.style.top) + 5 + 'px';
//            }
//
//            function moveSelection(evt) {
//                console.log("event: "+evt.keyCode)
//                switch (evt.keyCode) {
//                    case 37:
//                    leftArrowPressed();
//                    break;
//                    case 39:
//                    rightArrowPressed();
//                    break;
//                    case 38:
//                    upArrowPressed();
//                    break;
//                    case 40:
//                    downArrowPressed();
//                    break;
//                    }
//                };
//
//        function docReady()
//        {
//
//          window.addEventListener('keydown', moveSelection);
//        }
//$( document ).ready(function() {
//    docReady();
//});

//https://jsfiddle.net/macloo/ewag8ews/
$(document).on('keydown', function(e) {
  // e stands for "event" - the event is the keypress
  // e.key means the key that was pressed
  console.log("event: "+e.key);
  switch (e.key) {
    // left arrow pressed
    case "ArrowLeft":
      $('#moving').animate({
        left: "-=10px"
      }, 'fast');
      break;
      // up arrow pressed
    case "ArrowUp":
      $('#moving').animate({
        top: "-=10px"
      }, 'fast');
      break;
      // right arrow pressed
    case "ArrowRight":
      $('#moving').animate({
        left: "+=10px"
      }, 'fast');
      break;
      // down arrow pressed
    case "ArrowDown":
      $('#moving').animate({
        top: "+=10px"
      }, 'fast');
      break;
  }
});
