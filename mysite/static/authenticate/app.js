const draggables = document.querySelectorAll('.draggable');
const containers = document.querySelectorAll('.letterbody')



draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging')
        console.log('Dragging');
    })
    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging')

    })
})

letterbody.addEventListener('dragover', e => {
    console.log('Dragover');
    e.preventDefault()
    const afterElement = getDragAfterElement(letterbody, e.clientY)
    const draggable = document.querySelector('.dragging')
    letterbody.appendChild(draggable)
})

function getDragAfterElement(letterbody, y) {
    const draggableElements = [...letterbody.querySelectorAll('draggable:not(.dragging')]
}

function Export2Doc(element, filename = '') {
    var preHtml = "<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'><head><meta charset='utf-8'><title>Export HTML To Doc</title></head><body>";
    var postHtml = "</body></html>";
    var html = preHtml + document.getElementById(element).innerHTML + postHtml;

    var blob = new Blob(['\ufeff', html], {
        type: 'application/msword'
    });

    var url = 'data:application/vnd.ms-word;charset=utf-8,' + encodeURIComponent(html)

    filename = filename ? filename + '.doc' : 'document.doc';

    var downloadLink = document.createElement("a");

    document.body.appendChild(downloadLink);

    if (navigator.msSaveOrOpenBlob) {
        navigator.msSaveOrOpenBlob(blob, filename);
    } else {
        downloadLink.href = url;

        downloadLink.download = filename;

        downloadLink.click();
    }

    document.body.removeChild(downloadLink);
}