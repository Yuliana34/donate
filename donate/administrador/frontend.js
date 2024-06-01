
fetch('http://localhost:3306/ruta_vista_conectar_frontend/')
    .then(Response => Response.json())
    .then(data => console.log(data.mensaje))
    try{
        
    }
    catch(error => console.error('Error', error));