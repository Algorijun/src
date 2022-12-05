import Dropzone from "../../../static/dropzone"

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].Value
console.log(csrf)

const myDropzone = new Dropzone('#my-dropzone',  {
    url : '/upload/',
    init: function () {
        this.on ('sending', function(file,xhr,formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
    },

    maxFiles: 3,
    maxFilesize : 3,
    acceptedFiels: '.csv',
    
})