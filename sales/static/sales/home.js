console.log('hello world')

const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')

// in the home.html we have report-form Elem
const reportForm = document.getElementById('report_form')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = ` 
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

if (img) {
    reportBtn.classList.remove('not-visible')
}





// JS Eventlistener
reportBtn.addEventListener('click' , ()=>{
    console.log('clicked')
    // atrb for img   100% width fo modal body

    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)
    console.log(img.src)

    reportForm.addEventListener('submit', e=> {
        e.preventDefault() // 
        const formData = new FormData() // we need to send it 
        formData.append('csrfmiddlewaretoken' , csrf) 
        formData.append('name', reportName.value) 
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type : 'POST',
            url  : '/reports/save/', // we need get the url
            data : formData,
            success : function(response) {
                console.log(response)
                handleAlerts('success', 'Report created!')
            },
            error : function ( error) { 
                console.log(error)
                handleAlerts('danger', 'Something went wrong..')

            },
            processData : false,
            contentType : false,
        })
    })
})

// 