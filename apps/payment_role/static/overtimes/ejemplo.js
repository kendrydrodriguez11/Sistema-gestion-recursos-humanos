class Cobro {
    constructor(save) {
        this.save = save
        this.linea = 1
        this.cobro = {
            fecha_credito: '',
            credito: '',
            cliente: '',
            no_pagos: '',
            cuota: '',
            fecha_inicial: '',
            saldo: '',
            motivo: '',
            pagos: []
        }
    }

    agregarPago(fecha, cuota) {
        let pago = {}
        pago.numero = this.linea
        let fec = fecha.split("-")
        console.log(fec)
        pago.fecha = new Date(fec[2], fec[1], fec[0])
        pago.cuota = cuota
        pago.estado = 0
        this.cobro.pagos.push(pago)
        this.linea += 1
        this.presentar()
    }

    generarCuotas(deuda) {
        let primer_pago = new Date(deuda.fecha_inicial)
        //primer_pago=primer_pago.toString()
        let credito = parseFloat(deuda.credito)
        let num_pagos = parseInt(deuda.numero_pagos)
        let cuota = parseFloat(deuda.cuota)
        this.cobro.pagos = []
        for (let inicio = 1; inicio <= num_pagos; inicio++) {
            let pago = {}
            pago.numero = inicio
            let anio = primer_pago.getFullYear();
            let mes = ('0' + (primer_pago.getMonth() + 1)).slice(-2); // Agrega un cero inicial si es necesario
            let dia = ('0' + primer_pago.getDate()).slice(-2); // Agrega un cero inicial si es necesario
            console.log("fecF ", `${anio}-${mes}-${dia}`)
            pago.fecha = `${anio}-${mes}-${dia}`
            pago.cuota = cuota
            pago.estado = 0
            this.cobro.pagos.push(pago)
            console.log(pago)
            primer_pago.setDate(primer_pago.getDate() + 30)

        }
        console.log(this.cobro.pagos)
        this.presentar()
    }

    presentar() {
        let detalle = document.getElementById('detalle')
        detalle.innerHTML = ""
        this.cobro.pagos.forEach((pago) => {
            detalle.innerHTML += `<tr>
            <td>${pago.numero}</td>
            <td>${typeof pago.fecha === "string" ? pago.fecha : pago.fecha.toLocaleDateString()}   </td>
            <td>${pago.cuota}</td>
            <td>${pago.estado == 0 ? "Pendiente" : "Pagado"}</td>
            <td><a class="" href="#">💰</a></td>
     
           </tr>`
        });
    }

    registrar() {
        console.log("entro a registrar")
        if (this.cobro.pagos.length > 0) {
            this.cobro.fecha_credito = d.getElementById('id_fecha_credito').value
            this.cobro.cliente = d.getElementById('id_cliente').value
            this.cobro.credito = d.getElementById('id_credito').value
            this.cobro.saldo = d.getElementById('id_saldo').value
            this.cobro.no_pagos = d.getElementById('id_numero_pagos').value
            this.cobro.cuota = d.getElementById('id_cuota').value
            this.cobro.fecha_inicial = d.getElementById('id_fecha_primer_pago').value
            this.cobro.motivo = d.getElementById('id_motivo').value
            console.log(this.cobro)
            let csrf = d.querySelector('[name=csrfmiddlewaretoken]').value
            console.log(csrf)
            console.log(this.save)

            const grabarVenta = async (url) => {
                console.log(url)
                try {
                    const res = await fetch(url,
                        {
                            method: 'POST',
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest',
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrf,
                            },
                            body: JSON.stringify(this.cobro)
                        });
                    const post = await res.json();
                    console.log(post.grabar);
                    alert("Factura grabada Satisfactoriamente")

                    window.location.href = "/cuentas_cobrar/"
                } catch (error) {
                    console.log("error=>", error);
                    alert(error)
                }
            };
            grabarVenta(this.save);
        } else {
            alert("no ha registrado los datos")
        }
    }
}

//  Manejo Del DOM
let d = document
d.addEventListener("DOMContentLoaded", e => {
    console.log("Pagina cargada")
    console.log("{% url 'cuentas_cobrar' %}")
    let cobro = new Cobro(save)
    // seleccion de elementos
    let $form = d.getElementById('form')
    let $btnGenerar = d.getElementById('btnGenerar')
    let $btnPago = d.getElementById('btnPago')
    let $txtCre = d.getElementById('id_credito')
    let $txtSal = d.getElementById('id_saldo')
    let $txtCut = d.getElementById('id_cuota')
    let $txtNp = d.getElementById('id_numero_pagos')
    // manejadores de eventos
    $btnGenerar.addEventListener('click', (e) => {
        console.warn(e.target)
        let credito = {}
        credito.fecha_inicial = d.getElementById('id_fecha_primer_pago').value
        credito.credito = d.getElementById('id_credito').value
        credito.numero_pagos = d.getElementById('id_numero_pagos').value
        credito.cuota = d.getElementById('id_cuota').value
        console.log(credito)
        cobro.generarCuotas(credito)
    })
    $btnPago.addEventListener('click', (e) => {
        let fecha = d.getElementById('cboFecha')
        fecha = fecha.options[fecha.selectedIndex].text
        let cuota = d.getElementById('idCuota').value
        console.log(fecha, cuota)
        cobro.agregarPago(fecha, parseFloat(cuota))
    })
    $txtCre.addEventListener('change', (e) => {
        $txtSal.value = e.target.value
        $txtCut.value = (e.target.value / $txtNp.value).toFixed(2)
    })
    $txtNp.addEventListener('change', (e) => {
        $txtCut.value = ($txtCre.value / e.target.value).toFixed(2)
    })
    $form.addEventListener('submit', (e) => {
        e.preventDefault()
        cobro.registrar()
    })

})
