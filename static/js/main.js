
//globales
var NumPersonas;
var NumInfectados;
var NumVacunados;
var NumComorbilidades;
var NumTiempo;
var cv;
var ctx;
var listAgentesImages = [];
var timerID;
var tiempo = 50;
var contador = 1;

var imgObjects;

var timerPasoID;
var contadorPaso = 0;
//posiciones
var xs = [];
var ys = [];
var xs_last = [];
var ys_last = [];
var distancias = [];
var distancias_x = [];
var distancias_y = [];
var pasos = [];
var pasos_x = [];
var pasos_y = [];
var angulos = [];
var signos_x = [];
var signos_y = [];
var first_time = true;
var first_draw = true;
var paso = 10;
var contadorTiempoPasado = 0;

//contadoores gráfica
var cont_recuperados = new Array();
var cont_decesos = new Array();
var cont_enfermos = new Array();
var cont_inmunes = new Array();
var cont_suceptibles = new Array();
var dias = new Array();

var cont_aux_recuperados = 0;
var cont_aux_decesos = 0;
var cont_aux_enfermos = 0;
var cont_aux_inmunes = 0;
var cont_aux_suceptibles = 0;
var cont_personas_sanas_inicial = 0;
var cont_personas_sanas = 0;
var poblacion_total = 0;

var aux_decesos = new Array();     //vector que guarda los decesos redi-bujados
var aux_recuperados = new Array(); //vector que guarda los recuperados redi-bujados

function move_step(){
    if(contadorPaso < 10){
        ctx.clearRect(0, 0, cv.width, cv.height);
        for (var i = 0; i < imgObjects.length; i++) {
            //obtener las componentes x y y
            ///var comp_x = parseInt((signos_x[i]*pasos[i]*(contadorPaso))*Math.cos(angulos[i]) + xs_last[i]);
            ///var comp_y = parseInt((signos_y[i]*pasos[i]*(contadorPaso))*Math.sin(angulos[i]) + ys_last[i]);
            var comp_x = parseInt((signos_x[i]*pasos_x[i]*(contadorPaso)) + xs_last[i]);
            var comp_y = parseInt((signos_y[i]*pasos_y[i]*(contadorPaso)) + ys_last[i]);
            //console.log("comp_x: " + comp_x.toString());
            //console.log("comp_y: " + comp_y.toString());
            ctx.drawImage(imgObjects[i], comp_x, comp_y);
        }
        contadorPaso++;
    }
    else{
        contadorPaso = 0;
        clearInterval(timerPasoID);
        //volver a activar timer que va a siguiente
        timerID = setInterval(siguiente, 200);
        //aumentar contador
        contadorTiempoPasado++;
        tiempopasado = document.getElementById("sliderTime");
        tiempopasado.value = contadorTiempoPasado;
    }
}

function draw_agentes(agentes){
    console.log("draw_agentes");
    cv = document.getElementById("dibujo");
    ctx = cv.getContext("2d");
    

    //si ya no es la primera vez, hacer el volcado de coordenadas
    if(!first_time){
        xs_last = [];
        ys_last = [];
        for (var j = 0; j < xs.length; j++){
            xs_last.push(xs[j]);
            ys_last.push(ys[j]);
        }
        //
        console.log("RESPALDO:");
        console.log(xs_last);
        console.log(ys_last);
    }

    //dibujar imagen
    var nombres = [];
    xs = [];
    ys = [];
    var img = [];

    for(const agente in agentes){
        console.log(agentes[agente].nombre);
        let nombreAgente = agentes[agente].nombre;
        nombres.push(nombreAgente);
        //obtener la posicion
        listaPosicion = agentes[agente].posicion.split(",");
        var x = parseInt(listaPosicion[0]) * 10;
        xs.push(x);
        var y = parseInt(listaPosicion[1]) * 10;
        ys.push(y);
    
        //ver tipo de imagen
        if(agentes[agente].deceso === "False"){
            if(agentes[agente].infectado === "True"){
                if(agentes[agente].asintomatico === "True"){
                    img.push('/static/images/person-yellow.png');
                }
                else{
                    if(agentes[agente].conmorbolidad === "True"){
                        img.push('/static/images/person-red.png');
                    }
                    else{
                        img.push('/static/images/person-yellow.png');
                    }
                }
            }
            else{
                 cont_aux_recuperados = cont_aux_recuperados + 1;
                 if(contador == 1)
                 {
                       cont_personas_sanas_inicial = cont_personas_sanas_inicial + 1;
                 }

                if(agentes[agente].inmunidad === "True"){
                cont_aux_inmunes = cont_aux_inmunes + 1;
                    img.push('/static/images/person-blue.png');
                }
                else{
                    cont_personas_sanas = cont_personas_sanas + 1;
                    cont_aux_suceptibles = cont_aux_suceptibles + 1;
                    img.push('/static/images/person-green.png');
                }
            }
        }
        else{
            cont_aux_decesos = cont_aux_decesos + 1;
            img.push('/static/images/person-black.png');
        }
        ////
        /*agente_img = new Image();
        agente_img.src = '/static/images/person-black.png';
        agente_img.onload = function(){
            ctx.drawImage(agente_img, x*10, y*10);
        }
        listAgentesImages.push({[nombreAgente] : agente_img});*/
    }

    poblacion_total = NumPersonas;
    cont_aux_enfermos = poblacion_total - cont_aux_suceptibles - cont_aux_inmunes - cont_aux_decesos;
    //cont_aux_decesos = poblacion_total - cont_aux_suceptibles - cont_aux_enfermos - cont_aux_inmunes;
    //cont_aux_recuperados = poblacion_total - cont_aux_enfermos - cont_aux_decesos - cont_aux_suceptibles;
    if( cont_personas_sanas < cont_personas_sanas_inicial )
    {
        cont_personas_sanas_inicial = cont_personas_sanas;
    }
    cont_aux_recuperados = Math.abs(cont_personas_sanas_inicial - cont_aux_recuperados);

    console.log("ORIGINALES:");
    console.log(xs);
    console.log(ys);

    //sacar ángulo y distancia
    distancias = [];
    distancias_x = [];
    distancias_y = [];
    angulos = [];
    signos_x = [];
    signos_y = [];
    for (var k = 0; k < xs.length; k++){
        var temp_x = xs[k]-xs_last[k];
        distancias_x.push(Math.abs(temp_x));
        var temp_y = ys[k]-ys_last[k];
        distancias_y.push(Math.abs(temp_y));
        //signos
        if(xs[k] >= xs_last[k]){
            signos_x.push(1);
        }
        else{
            signos_x.push(-1);
        }

        if(ys[k] >= ys_last[k]){
            signos_y.push(1);
        }
        else{
            signos_y.push(-1);
        }

        distancias.push(Math.sqrt(Math.pow(temp_x,2)+Math.pow(temp_y,2)));
        angulos.push(Math.atan(temp_y/temp_x));
    }
    console.log("ángulo y distancia");
    console.log(distancias);
    console.log(angulos);

    //calcular pasos
    pasos = [];
    pasos_x = [];
    pasos_y = [];
    for (var l = 0; l < distancias.length; l++){
        pasos.push(distancias[l]/paso);
        pasos_x.push(distancias_x[l]/paso);
        pasos_y.push(distancias_y[l]/paso);
    }

    //crear las imágenes
    imgObjects = img.map(function(i){
        var im = new Image();
        im.src = i;
        return im;
    });
    //console.log(listAgentesImages);
    Promise.all(imgObjects.map(function(image) {
        return new Promise(function(resolve, reject) {
          image.onload = resolve;
        });
      }))
      .then(function() {
        if(first_draw){
            for (var i = 0; i < imgObjects.length; i++) {
                //var img = imgObjects[i];
                ctx.drawImage(imgObjects[i], xs[i], ys[i]);
                listAgentesImages.push({[nombres[i]] : imgObjects[i]});
            }
            first_draw = false;
        }
        else{
            //aqui se va repintando todo!!!
            //aqui debería hacer un for o un doble for??
            //for 1 es un for de 10
            //for 2 es el for de los imgObjects
            // for (var m = 0; m < paso; m++){
            //     ctx.clearRect(0, 0, cv.width, cv.height);
            //     for (var i = 0; i < imgObjects.length; i++) {
            //         //obtener las componentes x y y
            //         var comp_x = parseInt((pasos[i]*(m))*Math.cos(angulos[i]) + xs[i]);
            //         var comp_y = parseInt((pasos[i]*(m))*Math.sin(angulos[i]) + ys[i]);
            //         ctx.drawImage(imgObjects[i], comp_x, comp_y);
            //     }
            // }
            //crear el timer
            timerPasoID = setInterval(move_step, 50);
            console.log("xs_last: ");
            console.log(xs_last);
            console.log("ys_last: ");
            console.log(ys_last);
        }
        //console.log(listAgentesImages[0][0]);
      });
      first_time = false;
}

function postData(url = '', data = {}){
    fetch(url, {
    method: 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
        'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
    }).then((response) => response.json()
    .then((result) => {
        console.log(result);
        draw_agentes(result);
        //activar timer
        timerID = setInterval(siguiente, 150);
    }));
}

var siguiente = function(){
    if(contador < tiempo){
        dias.push(contador);

        ctx.clearRect(0, 0, cv.width, cv.height);
        fetch("/tick", {
            method: 'GET',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            }).then((response) => response.json()
            .then((result) => {
                console.log(result);
                //prueba --
                clearInterval(timerID);
                draw_agentes(result);
            }));

            aux_recuperados.push(cont_aux_recuperados);
            aux_decesos.push(cont_aux_decesos);

            if(aux_recuperados[contador] == aux_recuperados[contador -1])
            {
                cont_aux_recuperados = 0;
            }
            else
            {
                cont_aux_recuperados = Math.abs(aux_recuperados[contador] - aux_recuperados[contador - 1]);
            }

            if(aux_decesos[contador] == aux_decesos[contador -1])
            {
                cont_aux_decesos = 0;
            }
            else
            {
                cont_aux_decesos = aux_decesos[contador] - aux_decesos[contador - 1];
            }

            cont_recuperados.push(cont_aux_recuperados);
            cont_decesos.push(cont_aux_decesos);
            cont_enfermos.push(cont_aux_enfermos);
            cont_inmunes.push(cont_aux_inmunes);
            cont_suceptibles.push(cont_aux_suceptibles);
            Grafica_recuperados(dias,cont_recuperados);
            Grafica_decesos(dias,cont_decesos);
            Grafica_enfermos(dias,cont_enfermos);
            Grafica_inmunes(dias,cont_inmunes);
            Grafica_suceptibles(dias,cont_suceptibles);
            cont_aux_recuperados = 0;
            cont_aux_decesos = 0;
            cont_aux_enfermos = 0;
            cont_aux_inmunes = 0;
            cont_personas_sanas = 0;
            cont_aux_suceptibles = 0;

            contador++;
    }
    else{
        clearInterval(timerID);
        alert("Tiempo de simulación terminado");
        //fin de todo / reiniciar todo
        //globales
        listAgentesImages = [];
        tiempo = 50;
        contador = 0;

        contadorPaso = 0;
        //posiciones
        xs = [];
        ys = [];
        xs_last = [];
        ys_last = [];
        distancias = [];
        distancias_x = [];
        distancias_y = [];
        pasos = [];
        pasos_x = [];
        pasos_y = [];
        angulos = [];
        signos_x = [];
        signos_y = [];
        first_time = true;
        first_draw = true;
        paso = 10;
        contadorTiempoPasado = 0;
    }
    

}

var getData = function(){
    console.log("Entra a getData");
    //obtener los datos de los sliders
    NumPersonas = document.getElementById("NumPersonas").value;
    NumInfectados = document.getElementById("NumInfectados").value;
    NumVacunados = document.getElementById("NumVacunados").value;
    NumComorbilidades = document.getElementById("Comorbilidades").value;
    NumTiempo = document.getElementById("Dias").value;
    tiempo = NumTiempo;

    aux_recuperados.push(0);
    aux_decesos.push(0);

    //poner el range
    tiempopasado = document.getElementById("sliderTime");
    tiempopasado.max = tiempo;
    tiempopasado.value = 0;
    //enviar la peticion
    const bodyInfo = {
        "NumPersonas" : NumPersonas,
        "NumInfectados" : NumInfectados,
        "NumVacunados" : NumVacunados,
        "NumComorbilidades" : NumComorbilidades,
        "NumTiempo" : NumTiempo
    };
    postData('/sendInfo', bodyInfo);
}

function getTick(){
    var requestOptions = {
        method: "GET",
        mode: "cors",
    }
    fetch(
        "/tick",
        requestOptions
    )
    .then((response) => response.json())
    .then((result) => {
        console.log(result);
    })
    .catch((error) => console.log("error", error));
}

function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
}
  
function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
}

function Grafica_recuperados(ctd_dias,ctd_recuperados){

    Graph1 = document.getElementById("myChart1");
    ctxGraph1 = Graph1.getContext("2d");

  new Chart(ctxGraph1,{
            type:"line",
            data:{
                //labels:[1, 20, 50, 60],
                labels:ctd_dias,
                datasets:[
              {
                   label:'Recuperados',
                   borderColor:'green',
                   //data:[5, 10, 17, 20],
                   data:ctd_recuperados,
                }]
            },
            options:{
        //        events: [],
               responsive: false,
                events: ['mouseout', 'click', 'touchstart', 'touchmove'],
                title:{
                    display: true,
                    text: 'Personas recuperadas por dia',
                    fontSize: 15,
                    padding: 30,
                    fontColor: '#12619c',
                },
                legend:{
                    position: 'bottom',
                    labels:{
                        padding: 20,
                        boxWidth: 15,
                        fontFamily: 'system-ui',
                        fontColor: 'black',
                    }
                },
                layout:{
                    padding:{
                        right: 10,
                    }
                },
                tooltips:{
                    backgroundColor: '#0584f6',
                    titleFontSize: 10,
                    xPadding: 20,
                    yPadding: 20,
                    bodyFontSize: 10,
                    bodySpacing: 10,
                    mode: 'x',
                },
                elements:{
                    line:{
                        borderWidth: 5,
                        fill: false,
                    },
                    point:{
                    radius: 3,
                    borderWidth: 2,
                    backgroundColor: 'white',
                    hoverRadius: 5,
                    hoverBorderWidth: 2,
                    },
                },
                scales:{
                    yAxes:[{
                            ticks:{
                                beginAtZero:true
                            }
                    }],
                    xAxes:[{
                        gridLines:{
                            display: false,
                        }
                    }]
                }
            }
        });

}

function Grafica_decesos(ctd_dias,ctd_decesos){

    Graph2 = document.getElementById("myChart2");
    ctxGraph2 = Graph2.getContext("2d");

  new Chart(ctxGraph2,{
            type:"line",
            data:{
                //labels:[1, 20, 50, 60],
                labels:ctd_dias,
                datasets:[
                {
                   label:'Decesos',
                   borderColor:'black',
                   //data:[1, 20, 30, 40],
                   data:ctd_decesos,
                }]
            },
            options:{
        //        events: [],
               responsive: false,
                events: ['mouseout', 'click', 'touchstart', 'touchmove'],
                title:{
                    display: true,
                    text: 'Personas muertas por dia',
                    fontSize: 15,
                    padding: 30,
                    fontColor: '#12619c',
                },
                legend:{
                    position: 'bottom',
                    labels:{
                        padding: 20,
                        boxWidth: 15,
                        fontFamily: 'system-ui',
                        fontColor: 'black',
                    }
                },
                layout:{
                    padding:{
                        right: 10,
                    }
                },
                tooltips:{
                    backgroundColor: '#0584f6',
                    titleFontSize: 10,
                    xPadding: 20,
                    yPadding: 20,
                    bodyFontSize: 10,
                    bodySpacing: 10,
                    mode: 'x',
                },
                elements:{
                    line:{
                        borderWidth: 5,
                        fill: false,
                    },
                    point:{
                    radius: 3,
                    borderWidth: 2,
                    backgroundColor: 'white',
                    hoverRadius: 5,
                    hoverBorderWidth: 2,
                    },
                },
                scales:{
                    yAxes:[{
                            ticks:{
                                beginAtZero:true
                            }
                    }],
                    xAxes:[{
                        gridLines:{
                            display: false,
                        }
                    }]
                }
            }
        });

}

function Grafica_enfermos(ctd_dias,ctd_enfermos){

    Graph3 = document.getElementById("myChart3");
    ctxGraph3 = Graph3.getContext("2d");

  new Chart(ctxGraph3,{
            type:"line",
            data:{
                //labels:[1, 20, 50, 60],
                labels:ctd_dias,
                datasets:[
                 {
                   label:'Enfermos',
                   borderColor:'red',
                   //data:[1, 10, 30, 100],
                   data:ctd_enfermos,
                }]
            },
            options:{
        //        events: [],
               responsive: false,
                events: ['mouseout', 'click', 'touchstart', 'touchmove'],
                title:{
                    display: true,
                    text: 'Personas enfermas por dia',
                    fontSize: 15,
                    padding: 30,
                    fontColor: '#12619c',
                },
                legend:{
                    position: 'bottom',
                    labels:{
                        padding: 20,
                        boxWidth: 15,
                        fontFamily: 'system-ui',
                        fontColor: 'black',
                    }
                },
                layout:{
                    padding:{
                        right: 10,
                    }
                },
                tooltips:{
                    backgroundColor: '#0584f6',
                    titleFontSize: 10,
                    xPadding: 20,
                    yPadding: 20,
                    bodyFontSize: 10,
                    bodySpacing: 10,
                    mode: 'x',
                },
                elements:{
                    line:{
                        borderWidth: 5,
                        fill: false,
                    },
                    point:{
                    radius: 3,
                    borderWidth: 2,
                    backgroundColor: 'white',
                    hoverRadius: 5,
                    hoverBorderWidth: 2,
                    },
                },
                scales:{
                    yAxes:[{
                            ticks:{
                                beginAtZero:true
                            }
                    }],
                    xAxes:[{
                        gridLines:{
                            display: false,
                        }
                    }]
                }
            }
        });
}

function Grafica_inmunes(ctd_dias,ctd_inmunes){

    Graph4 = document.getElementById("myChart4");
    ctxGraph4 = Graph4.getContext("2d");

  new Chart(ctxGraph4,{
            type:"line",
            data:{
                //labels:[1, 20, 50, 60],
                labels:ctd_dias,
                datasets:[
                 {
                   label:'Inmunes',
                   borderColor:'blue',
                   //data:[1, 10, 30, 100],
                   data:ctd_inmunes,
                }]
            },
            options:{
        //        events: [],
               responsive: false,
                events: ['mouseout', 'click', 'touchstart', 'touchmove'],
                title:{
                    display: true,
                    text: 'Personas inmunes en el dia',
                    fontSize: 15,
                    padding: 30,
                    fontColor: '#12619c',
                },
                legend:{
                    position: 'bottom',
                    labels:{
                        padding: 20,
                        boxWidth: 15,
                        fontFamily: 'system-ui',
                        fontColor: 'black',
                    }
                },
                layout:{
                    padding:{
                        right: 10,
                    }
                },
                tooltips:{
                    backgroundColor: '#0584f6',
                    titleFontSize: 10,
                    xPadding: 20,
                    yPadding: 20,
                    bodyFontSize: 10,
                    bodySpacing: 10,
                    mode: 'x',
                },
                elements:{
                    line:{
                        borderWidth: 5,
                        fill: false,
                    },
                    point:{
                    radius: 3,
                    borderWidth: 2,
                    backgroundColor: 'white',
                    hoverRadius: 5,
                    hoverBorderWidth: 2,
                    },
                },
                scales:{
                    yAxes:[{
                            ticks:{
                                beginAtZero:true
                            }
                    }],
                    xAxes:[{
                        gridLines:{
                            display: false,
                        }
                    }]
                }
            }
        });
}

function Grafica_suceptibles(ctd_dias,ctd_suceptibles){

  Graph5 = document.getElementById("myChart5");
  ctxGraph5 = Graph5.getContext("2d");

  new Chart(ctxGraph5,{
            type:"line",
            data:{
                //labels:[1, 20, 50, 60],
                labels:ctd_dias,
                datasets:[
                 {
                   label:'Suceptibles',
                   borderColor:'orange',
                   //data:[1, 10, 30, 100],
                   data:ctd_suceptibles,
                }]
            },
            options:{
        //        events: [],
               responsive: false,
                events: ['mouseout', 'click', 'touchstart', 'touchmove'],
                title:{
                    display: true,
                    text: 'Personas suceptibles en el dia',
                    fontSize: 15,
                    padding: 30,
                    fontColor: '#12619c',
                },
                legend:{
                    position: 'bottom',
                    labels:{
                        padding: 20,
                        boxWidth: 15,
                        fontFamily: 'system-ui',
                        fontColor: 'black',
                    }
                },
                layout:{
                    padding:{
                        right: 10,
                    }
                },
                tooltips:{
                    backgroundColor: '#0584f6',
                    titleFontSize: 10,
                    xPadding: 20,
                    yPadding: 20,
                    bodyFontSize: 10,
                    bodySpacing: 10,
                    mode: 'x',
                },
                elements:{
                    line:{
                        borderWidth: 5,
                        fill: false,
                    },
                    point:{
                    radius: 3,
                    borderWidth: 2,
                    backgroundColor: 'white',
                    hoverRadius: 5,
                    hoverBorderWidth: 2,
                    },
                },
                scales:{
                    yAxes:[{
                            ticks:{
                                beginAtZero:true
                            }
                    }],
                    xAxes:[{
                        gridLines:{
                            display: false,
                        }
                    }]
                }
            }
        });
}
