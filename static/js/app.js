document.querySelector('.dir').addEventListener('click', function(e) {
    e.preventDefault()
})

function getNumberOfFiles() {
    $.ajax({
      type: 'GET',
      url: '/files_count',
      success: function (response) {
        $('#files-link').text('Files (' + response.count + ')');
      }
    });
  }
  