/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/customers';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.customers.forEach(item => insertList(item.name, 
                                                item.age, 
                                                item.gender,
                                                item.tenure,
                                                item.monthly_charges,
                                                item.contract_type,
                                                item.internet_service,
                                                item.total_charges,
                                                item.tech_support,
                                                item.churn
                                              ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (name, age, gender, tenure, monthly_charges,
                        contract_type, internet_service, total_charges, 
                        tech_support) => {
    
  const formData = new FormData();
  formData.append('name', name);
  formData.append('age', age);
  formData.append('gender', gender);
  formData.append('tenure', tenure);
  formData.append('monthly_charges', monthly_charges);
  formData.append('contract_type', contract_type);
  formData.append('internet_service', internet_service);
  formData.append('total_charges', total_charges);
  formData.append('tech_support', tech_support);

  let url = 'http://127.0.0.1:5000/customer';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/customer?name='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let name = document.getElementById("name").value;
  let age = document.getElementById("age").value;
  let gender = getComboValue("gender");
  let tenure = document.getElementById("tenure").value;
  let monthly_charges = document.getElementById("monthly_charges").value;
  let contract_type = getComboValue("contract_type");
  let internet_service = getComboValue("internetService");
  let total_charges = document.getElementById("total_charges").value;
  let tech_support = getComboValue("tech_support");

  // Verifique se o nome do cliente já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/customer?nome=${name}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then((data) => { alert(data.age); 
      if (data && data.name === name) {
        alert("O paciente já está cadastrado.\nCadastre o paciente com um nome diferente ou atualize o existente.");
      } else if (name === '') {
        alert("O nome do cliente não pode ser vazio!");
      }else if (isNaN(gender)) {
        alert("O genero do cliente tem que ser escolhido!");
      }else if (isNaN(contract_type)) {
        alert("O tipo de contrato tem que ser escolhido!");
      }else if (isNaN(internet_service)) {
        alert("O tipo de serviço tem que ser escolhido!");
      }else if (isNaN(tech_support)) {
        alert("O suporte técnico tem que ser escolhido!");
      }else if (isNaN(age) || isNaN(tenure) || isNaN(monthly_charges)) {
        alert("Esse(s) campo(s) precisam ser números!");
      }else {
        insertList(name, age, gender, tenure, monthly_charges, contract_type, internet_service, total_charges, tech_support);
        postItem(name, age, gender, tenure, monthly_charges, contract_type, internet_service, total_charges, tech_support);
        alert("Item adicionado!");
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const contractMap = {
  1: 'Mês a mês',
  2: 'Um ano',
  3: 'Dois anos'
};

const serviceMap = {
  1: 'DSL',
  2: 'Fibra Óptica',
  3: 'Nenhum'
}

const insertList = (name, age, gender, tenure, monthly_charges, contract_type, internet_service, total_charges, tech_support, churn) => {

  gender = gender === 1 ? 'Feminino' : 'Masculino';
  contract_type = contractMap[contract_type];
  internet_service = serviceMap[internet_service];
  tech_support = tech_support === 1 ? 'Sim' : 'Não';

  var item = [name, age, gender, tenure, monthly_charges, contract_type, internet_service, tech_support, total_charges, churn];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  document.getElementById("name").value = "";
  document.getElementById("age").value = "";
  document.getElementById("gender").value = "";
  document.getElementById("tenure").value = "";
  document.getElementById("monthly_charges").value = "";
  document.getElementById("contract_type").value = "";
  document.getElementById("internetService").value = "";
  document.getElementById("total_charges").value = "";
  document.getElementById("tech_support").value = "";


  removeElement();
}

/*
  --------------------------------------------------------------------------------------
  Função para recuperar items selecionado do combo
  --------------------------------------------------------------------------------------
*/

function getComboValue(comboName) 
{
  var select = document.getElementById(comboName);
  var value = select.options[select.selectedIndex].value;
  return value;
}

/*
  --------------------------------------------------------------------------------------
  Função para calcular o valor items total_changes
  --------------------------------------------------------------------------------------
*/

function calculateTotal() {
  // Obtém os valores dos inputs
  var tenure = parseFloat(document.getElementById('tenure').value) || 0;
  var monthlyCharges = parseFloat(document.getElementById('monthly_charges').value) || 0;

  // Calcula e define o valor no input total_charges
  document.getElementById('total_charges').value = monthlyCharges * tenure;
}