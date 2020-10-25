var GLOBAL_FLAG = 0


target_age  = [" grim darkness", " Church and the Thy word", " Memmi and Esded", " Konrad Witz", " Bosch", " Michelangelo", " Vasari", " Aert",
" Pussino", " Fradel", " Coccorante", " Issel" ," Aivazovsky"]

age  = ["1300 and older", "1300-1350", "1351-1400", "1401-1450", "1451-1500", "1501-1550", "1551-1600", "1601-1650", "1651-1700", "1701-1750",
  "1751-1800", "1801-1850", "1851-1900"]
var FILE_STATUS = 0
var REFRESHMENT = 0
function checkStatus() {
   FILE_STATUS = document.getElementById("image-file").files.length;
 //   alert(document.getElementById("image-file").files.length)
  if ((FILE_STATUS != 0) && (REFRESHMENT == 1)) {

      let file = document.getElementById("image-file").files[0];
      let formData = new FormData();
      let data = {
          complex_title: 'Подстанция ПОС-49',
          event_file:  './data/2_faza_VL.cff',
          event_title: 'КЗ',
          event_description: '.'
      }
      let url = 'https://cors-anywhere.herokuapp.com/' + 'http://95.217.164.134/worker/register-event'
      fetch(url, {
          method: 'POST',
          body: JSON.stringify(data),
  })
        .then((response) => {
           return response.json()
        }).then((data) => {
            alert(data.ok);
      })
      REFRESHMENT = 0;
  }
}

window.onload = function() {
  $("#button-back").click(function() {
    alert()
  $("body").fadeOut(1000);
  setTimeout(function(){location.href="/"} , 1500);
});

$("body").fadeOut(1)
$("body").fadeIn(1200)

let fake = $('.req')



fake.click(function(e) {
  e.preventDefault()

  $('#image-file').trigger('click');
  REFRESHMENT = 1;
})
setInterval(checkStatus,1);


  let dropArea = document.getElementById('dropzone')

;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false)
})

function preventDefaults (e) {
  e.preventDefault()
  e.stopPropagation()
}

;['dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false)
})
;['drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false)
})
function highlight(e) {
  $(".zone").fadeIn(300)
}
function unhighlight(e) {
 $(".zone").fadeOut(300)
}

function uploadFile(file) {
  $(".req").fadeOut(300)
  let url = '/upload'
  let formData = new FormData()
  formData.append('file', file)

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then((response) => {
      return response
  }).then((data) => {

    setTimeout(function(){location.href="/foo"} , 1500);
  })
  .catch(() => {})
}

function handleFiles(files) {
  ([...files]).forEach(uploadFile)
}

dropArea.addEventListener('drop', handleDrop, false)
function handleDrop(e) {
  let dt = e.dataTransfer
  let files = dt.files
  handleFiles(files)
}



};
