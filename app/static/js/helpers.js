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