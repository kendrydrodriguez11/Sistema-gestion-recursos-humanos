// Variable de objetos
let d = document,c = console.log
// ------------------- carga inicial de la pagina ------------------------
d.addEventListener('DOMContentLoaded', function (e) {
  // Declaracion de variables
  let $employee = d.getElementById("id_employee")
  let $detailBody = d.getElementById('detalle')
  let $hoursDescription = d.getElementById('type_hours')
  let $btnAdd = d.getElementById("btnadd")
  let $btnGrabar = d.getElementById("btnGrabar")
  let $form = d.getElementById("form-container")
  let detailOvertime=[]
  if (detail_hours.length > 0){
    detailOvertime = detail_hours.map(item => {
      const { id: idHour, des: description, fac:factor, nh, vh:value } = item
      return { idHour, description, factor, nh, value }
    }) 
    present()
    totals()
  }
  // Declaracion de metodos
  // ---------- calcula el sobretiempo y lo añade al arreglo detailOvertime[] ----------
  const calculation = (idHour, factor, description, vh, nh) => {    
    const hours = detailOvertime.find(hour => hour.idHour == idHour)
    if (hours) {
      if (!confirm(`¿Ya existe ingresado ${hours.nh} =>  ${description}, Desea actualizar las ${description}?`)) return
      nh = nh + hours.nh  
      detailOvertime = detailOvertime.filter(hour => hour.idHour !== idHour);
    }
    let value = parseFloat((vh * factor * nh).toFixed(2))
    detailOvertime.push({ idHour, description, factor, nh, value })
    present()
    totals()
  }
// ------------------- actualiza el detalle del sobretiempo seleccionado -----------
  const reCalculation = (vh) => {
    detailOvertime= detailOvertime.map((item) => {
      let { idHour, description, factor, nh } = item
      let value = parseFloat((vh * factor * nh).toFixed(2))
      c({ idHour, description, factor, nh, value })
      return { idHour, description, factor, nh, value } 
    })
    present()
    totals()
  }
  // ---------------  borra el sobretiempo dado el id en el arreglo detailOvertime[] ------------
  const deleteHours = (id) => {
    detailOvertime = detailOvertime.filter((item) => item.idHour !== id)
    present()
    totals()
  }
 // recorre el arreglo detailOvertime y renderiza el detalle del sobretiempo -----------
  function present() {
    c("estoy en present()")
    let detalle = document.getElementById('detalle')
    detalle.innerHTML = ""
    detailOvertime.forEach((hours) => {
      detalle.innerHTML += `<tr>
            <td>${hours.idHour}</td>
            <td>${hours.description}</td>
            <td>${hours.factor}</td>
            <td>${hours.nh}</td>
            <td>💰${hours.value}</td>
            <td class="text-center ">
                <button rel="rel-delete" data-id="${hours.idHour}" class="text-danger" data-bs-toggle="tooltip" data-bs-title="Eliminar registro"><i class="bi bi-x-circle-fill"></i></button>
            </td>
          </tr>`
    });
  }
// ----- Sumariza del arreglo detailOvertime[] y lo renderiza en la tabla de la pagina -----
  function totals() {  
    const sumTotals = detailOvertime.reduce((acum, item) => {
      return acum + item.value;
    }, 0);
    d.getElementById('id_total').value = sumTotals.toFixed(2)
  }
  // ------------- manejo del DOM -------------
  $employee.addEventListener('change', async (e) => {
    let idEmployee = e.target.value
    if (!idEmployee) return
    idEmployee = parseInt(e.target.value)
    const employee = await fetchGet(`/payment_role/overtime/data_employee?idemp=${idEmployee}&action=value_hours`)
    if (!employee.ok) return alert("error en los datos")
    d.getElementById('id_value_hour').value = employee.data.hour
    d.getElementById('id_sucursal').value = employee.data.sucursal
    reCalculation(employee.data.hour)
  });
  // ---------- envia los datos del sobretiempo al backend por ajax para grabarlo ----------
  $form.addEventListener('submit', async (e) => {
    e.preventDefault()
    if (parseFloat(d.getElementById('id_total').value) > 0.00){ 
      const formData = new FormData($form)
      formData.append("detail", JSON.stringify(detailOvertime))
      const employee = await fetchPost(location.pathname, formData)
      if (!employee.ok) return c(employee.data)
      window.location = backUrl
    }else{
      alert("!!!Ingrese horas de sobretiempo para grabar!!!")
    }
  });
  // -------- registra las horas del sobretiempo en el arreglo detailOvertime[] ---------
  $btnAdd.addEventListener('click', (e) => {
    let numeHour = parseFloat(d.getElementById('id_nume_hours').value)
    if (numeHour > 0.00 && d.getElementById('id_calendar').value.length > 0){
      let typeHours = parseInt($hoursDescription.value)
      let valueHour = parseFloat(d.getElementById('id_value_hour').value)
      let factor = $hoursDescription.options[$hoursDescription.selectedIndex].dataset.value;
      factor = factor.replace(',', '.')
      let hoursDescription = $hoursDescription.options[$hoursDescription.selectedIndex].text
      calculation(typeHours, factor, hoursDescription, valueHour, numeHour)
      d.getElementById('id_nume_hours').value=""
    }else{
      alert("Faltan datos de ingresar( horas de sobretiempo o calendario de rol")
    }
  });
  //---- por delegacion de eventos seleccionada la fila de las horas del sobretiempo ----------
  //---- y la elimina del arreglo de detailOvertime[]  ---------
  $detailBody.addEventListener('click', (e) => {
    const fil = e.target.closest('button[rel=rel-delete]')
    if (fil) deleteHours(parseInt(fil.dataset.id))
  });
});
