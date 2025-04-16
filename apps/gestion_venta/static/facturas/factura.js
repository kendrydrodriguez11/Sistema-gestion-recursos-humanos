// Variable de objetos
let d = document, c = console.log
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener('DOMContentLoaded', function (e) {
    let cliente = d.getElementById("id_cliente")
    let $detailBody = d.getElementById('detalle')
    let $id_producto = d.getElementById('id_producto')
    let $btnAdd = d.getElementById("btnAgregar")
    let $form = d.getElementById("form-container")
    let iva = d.getElementById("id_iva").value
    let detailFactura = []
    if (detail_producto.length > 0) {
        detailFactura = detail_producto.map(item => {
            const { id: id_producto, des: descripcion, cant, prec, subtotal } = item
            return { id_producto, descripcion, cant, prec, subtotal }
        })
        present()
        totals()
    }
    // Declaracion de metodos
    // ---------- calcula la factura y lo añade al arreglo detailFactura[] ----------
    const calculation = (id_producto, descripcion, cant, prec) => {
        const producto = detailFactura.find(producto => producto.id_producto == id_producto)
        if (producto) {
            if (!confirm(`¿Ya existe ingresado ${producto.cant} =>  ${descripcion}, Desea actualizar las ${descripcion}?`)) return
            cant = cant + producto.cant
            detailFactura = detailFactura.filter(producto => producto.id_producto !== id_producto);
        }
        let subtotal = parseFloat((cant * prec).toFixed(2))
        detailFactura.push({ id_producto, descripcion, cant, prec, subtotal })
        present()
        totals()
    }
    // ---------------  borra el producto dado el id en el arreglo detailFactura[] ------------
    const deleteProducto = (id) => {
        detailFactura = detailFactura.filter((item) => item.id_producto !== id)
        present()
        totals()
    }
    // recorre el arreglo detailFactura y renderiza el detalle de la factura -----------
    function present() {
        let detalle = document.getElementById('detalle')
        detalle.innerHTML = ""
        detailFactura.forEach((producto) => {
            detalle.innerHTML += `<tr>
            <td>${producto.id_producto}</td>
            <td>${producto.descripcion}</td>
            <td>${producto.cant}</td>
            <td>${producto.prec}</td>
            <td>${producto.subtotal}</td>
            <td><button rel="rel-delete" class="btn btn-danger btn-sm" data-id="${producto.id_producto}">Eliminar</button></td>
            </tr>`
        })
    }

    // ------------------- calcula el total de la factura ---------------------------
    function totals() {
        let sumTotals = 0
        detailFactura.forEach((producto) => {
            sumTotals += producto.subtotal
        })
        document.getElementById('id_subtotal').value = sumTotals.toFixed(2)
        sumTotals += sumTotals * (iva / 100)
        document.getElementById('id_total').value = sumTotals.toFixed(2)
    }

    // ------------------- graba la factura ---------------------------
    $form.addEventListener('submit', async (e) => {
        e.preventDefault()
        if (parseFloat(d.getElementById('id_total').value) > 0.00) { 
            const formData = new FormData($form)
            formData.append("detail", JSON.stringify(detailFactura))
            const factura = await fetchPost(location.pathname, formData)
            if (!factura.ok) return alert("error en los datos")
            window.location = backUrl
        } else {
            alert("Debe ingresar productos a la factura")
        }
    })

    $btnAdd.addEventListener('click', (e) => {
        e.preventDefault()
        const cantidad = parseInt(document.getElementById('id_cantidad').value)
        if (cantidad <= 0) {
            alert("La cantidad debe ser mayor a cero")
            return
        }
        const producto = parseInt($id_producto.value)
        if (!producto) {
            alert("Debe seleccionar un producto")
            return
        }
        const precio = $id_producto.options[$id_producto.selectedIndex].dataset.value.replace(',', '.');
        const stock = $id_producto.options[$id_producto.selectedIndex].dataset.stock
        if (cantidad > stock) {
            alert(`La cantidad debe ser menor o igual al stock del producto: ${stock}`)
            return
        }
        const productoDescription = $id_producto.options[$id_producto.selectedIndex].text
        calculation(producto, productoDescription, cantidad, precio)
    })

    //---- por delegacion de eventos seleccionada la fila de los productos de la factura ----------
    $detailBody.addEventListener('click', function (e) {
        const fil = e.target.closest('button[rel=rel-delete]')
        if (!fil) return
        const id = parseInt(fil.dataset.id)
        deleteProducto(id)
    })
});