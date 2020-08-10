let boton = '';

function set_boton(value){
    console.log(value);
    this.boton = value;
}

function redireccionar_modal() {
    console.log('boton:'+this.boton);
    if(this.boton != undefined){
        document.getElementById(this.boton).click();
        this.boton = '';
    }else{
        document.getElementById('btn-send').click();
    }
}

$(function () {
    $('[data-toggle="popover"]').popover()
})

$(function(){
    $('#btn-submit').on('click', function(){
        $('#form-edit').validate({
            rules: {
                nombre: {required: true, minlength: 6, maxlength: 50},
                descripcion: { required: true, minlength: 10, maxlength: 100},
                precio: {required: true, number: true, min: 0}
            },
            messages: {
                nombre: {required: 'El campo es requerido', minlength: 'El tamaño mímino del nombre es de 6 caracteres', maxlength: 'El tamaño máximo del nombre es de 50 caracteres'},
                descripcion: { required: 'El campo es requerido', minlength: 'El tamaño mímino del nombre es de 10 caracteres', maxlength: 'El tamaño máximo del nombre es de 100 caracteres.' },
                precio: {required: 'El campo es requerido', number: 'Este campo es de tipo numérico', min: 'El precio debe ser positivo'}
            }
        });
    });
});

$(function(){
    $('#btn-submit-movement').on('click', function(){
        $('#form-add-movement').validate({
            rules: {
                cantidad: {required: true, digits: true, min: 1}
            },
            messages: {
                cantidad: {required: 'El campo es requerido', digits: 'Este campo es de tipo numérico', min: 'La cantidad debe ser positiva'}
            }
        });
    });
});