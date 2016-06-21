//FUNÇÃO DE REQUISIÇÃO AJAX PARA BUSCAR OS MORADORES DO CONDOMÍNIO DIGITADO
function get_data_condominium() {
	var value = $("#code").val() || $("#name").val();
    $.ajax({
        url : "codscc/"+value, // the endpoint
        type : "GET", // http method
        data : { value : value }, // data sent with the post request
		dataType: 'json', // Choosing a JSON datatype
        // handle a successful response
        success : function(data) {
			var residents = jQuery.parseJSON(data.residents);
			var condominium = jQuery.parseJSON(data.condominium);
			if (condominium[0] != null){
				$('#erro').html('');
				$('#moradores').html('');
				$('#code').val('');
				$('#name').val('');
				$('#condominio').html(
					condominium[0].fields.name_condominium
					//"<h5>Data última alteração: "+condominium[0].last_modified+"</h5>"+
					//"<h5>Quem alterou: "+condominium[0].who_modified+"</h5>"
					);
				for (var i=0; i < residents.length; i++){
					$("#moradores").append(					
						"<tr style='vertical-align: middle'>"+
						"<td><input type='checkbox' name='resident_email' value="+residents[i].fields.email_resident+"></td>"+
						"<td>"+residents[i].fields.num_un+"</th>"+
						"<td>"+residents[i].fields.type_of_resident+"</td>"+
						"<td>"+residents[i].fields.name_resident+"</td>"+
						"<td>"+residents[i].fields.email_resident+"</td>"+
						"</tr>"
					)				
				};
			}else{
				$('#erro').html(
					"<strong>Código ainda não cadastrado ou inválido!</strong>"
				);
			}
        },
		error : function(xhr,errmsg,err){
			console.log("#ERRO >> "+xhr + ":" + err);
		}
	});
};

//FUNÇÃO PARA O CHECKBOX DA TABELA DE RELAÇÃO DE MORADORES
$(document).ready(function(){
	$("#mytable #checkall").click(function () {
		if ($("#mytable #checkall").is(':checked')) {
			$("#mytable input[type=checkbox]").each(function () {
				$(this).prop("checked", true);
			});

		} else {
			$("#mytable input[type=checkbox]").each(function () {
				$(this).prop("checked", false);
			});
		}
	});
});

//FUNÇÃO PARA GERENCIAR O UPLOAD DE ARQUIVOS
$(function(){
	//http://www.fyneworks.com/jquery/multifile/#Usage
  $('#fileupload').MultiFile({
    accept:'jpg|png|bmp|doc|docx|xls|xlsx|pdf|txt|zip|rar', 
    maxsize:1024*10, 
    STRING: {
	  file: '$file',
      remove:'Remover',  
      selected:'Selecionado: $file', 
      denied:'Tipo de arquivo inválido: $ext!', 
      duplicate:'Arquivo ja selecionado:\n$file!',
	  toomuch: 'Os arquivos selecionados excedem o tamanho máximo permitido ($size)',
	  toobig:'$file é muito grande (max $size)'
    }
  });
});

//FUNÇÃO PARA EDITAR USUÁRIOS
function get_form_users(value) {
    $.ajax({
        url : "edit_user/"+value, // the endpoint
        type : "GET", // http method
        data : { value : value }, // data sent with the post request
		//dataType: 'json', // Choosing a JSON datatype
        // handle a successful response
        success : function(data) {
			$("#edit_users").html(
				data
			)
		}
	});
};


//FUNÇÃO PARA EDITAR A SENHA DO USUÁRIO
function change_pwd(value) {
	$.ajax({
        url : "change_pwd/"+value, // the endpoint
        type : "GET", // http method
        data : { value : value }, // data sent with the post request
		//dataType: 'json', // Choosing a JSON datatype
        // handle a successful response
        success : function(data) {
			$("#edit_users").html(
				data
			)
		}
	});
};

//FUNÇÃO PARA PEGAR O VALOR DO LISTBOX DA RELAÇÃO DE CONDOMÍNIOS E CRIAR
//UMA TABELA CONTENDO A RELAÇÃO DOS CONDÔMINOS DAQUELE CONDOMÍNIO
$('#id_condominium').on('change', function() {
	var value = this.value;
	$.ajax({
        url : "rel_residents/"+value, // the endpoint
        type : "GET", // http method
        data : { value : value }, // data sent with the post request
		dataType: 'json', // Choosing a JSON datatype
        // handle a successful response
        success : function(data) {
			var residents = jQuery.parseJSON(data.residents);
			$("#rel_residents").html('');
			$("#edit_resident").html('');
			for (var i=0; i < residents.length; i++){
				$("#rel_residents").append(
					"<tr style='vertical-align: middle'>"+
					"<td>"+residents[i].fields.num_un+"</td>"+
					"<td>"+residents[i].fields.type_of_resident+"</td>"+
					"<td>"+residents[i].fields.name_resident+"</td>"+
					"<td>"+residents[i].fields.email_resident+"</td>"+
					"<td><a href='#edit_resident' onclick='get_form_edit_resident("+residents[i].pk+")'><span class='glyphicon glyphicon-pencil' aria-hidden='true'></span></td>"+
					"</tr>"
				)				
			};
        },
		error : function(xhr,errmsg,err){
			console.log("#ERRO >> "+xhr + ":" + err);
		}
	});
});

function get_form_edit_resident(value) {
	$.ajax({
        url : "edit_resident/"+value, // the endpoint
        type : "GET", // http method
        data : { value : value }, // data sent with the post request
        // handle a successful response
        success : function(data) {
			$("#edit_resident").html(data);
        },
		error : function(xhr,errmsg,err){
			console.log("#ERRO >> "+xhr + ":" + err);
		}
	});
};