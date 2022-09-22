$(document).ready(function(){
    const url = '/api/users/';


    TableUsers=$('#TableUsers').DataTable({
        ajax:{
            url:url,
            dataSrc:''
        },
        columns:[
            {data: "email_users"},
            {data: "password_users"},
            {data: "isadmin_users"},
            {data: "username_users"},
            {data: null,
                render: function ( data, type, row ) {
                                      return '<button x-on:click="isConfirm = true" class="text-base BtnDelete rounded-l-none rounded-r-none border-l-0 border-r-0  hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer hover:bg-red-4000 hover:text-red-500 bg-teal-100 text-teal-700 border duration-200 ease-in-out border-teal-600 transition"><div class="flex leading-5"><svg class="svg-icon" viewBox="0 0 20 20"><path d="M17.114,3.923h-4.589V2.427c0-0.252-0.207-0.459-0.46-0.459H7.935c-0.252,0-0.459,0.207-0.459,0.459v1.496h-4.59c-0.252,0-0.459,0.205-0.459,0.459c0,0.252,0.207,0.459,0.459,0.459h1.51v12.732c0,0.252,0.207,0.459,0.459,0.459h10.29c0.254,0,0.459-0.207,0.459-0.459V4.841h1.511c0.252,0,0.459-0.207,0.459-0.459C17.573,4.127,17.366,3.923,17.114,3.923M8.394,2.886h3.214v0.918H8.394V2.886z M14.686,17.114H5.314V4.841h9.372V17.114z M12.525,7.306v7.344c0,0.252-0.207,0.459-0.46,0.459s-0.458-0.207-0.458-0.459V7.306c0-0.254,0.205-0.459,0.458-0.459S12.525,7.051,12.525,7.306M8.394,7.306v7.344c0,0.252-0.207,0.459-0.459,0.459s-0.459-0.207-0.459-0.459V7.306c0-0.254,0.207-0.459,0.459-0.459S8.394,7.051,8.394,7.306"></path></svg>Erase</div> </button>'; 
                }}
            ],
        responsive: true
    });


$('#formsUsers').submit(function(e){                         
    e.preventDefault(); //evita el comportambiento normal del submit, es decir, recarga total de la página
    Username=$('#Username').val();
    Email=$('#Email').val();
    IsAdmin=$('#admin').val();
    pasword=Username+"2020!"
    
    if(IsAdmin=="true"){
        IsAdmin=true;
    }
    else{
        IsAdmin=false;
    }

    var user = {
        "username": Username,
        "email": Email,
        "admin": IsAdmin,
        "password": pasword
    };


    var json = JSON.stringify(user);

        $.ajax({
          url: "/SignUp",
          type: "POST",
          datatype:"json",    
          contentType: "application/json",
          data: json,
          success: function(data) {
            TableUsers.ajax.reload(null, false);
            $('#TableUsers')[0].reset();
           }
           
        });			        
});
var row; 
$(document).on("click", ".BtnDelete", function(){	
    $("#TableUsers").trigger("reset");
    row = $(this).closest("tr");
    email= row.find('td:eq(0)').text();
    $("#id").val(email);

});


$('#tableDelete').submit(function(e){
    e.preventDefault(); //evita el comportambiento normal del submit, es decir, recarga total de la página

    email = $("#id").val();


    console.log(email);
    $.ajax({
        url: "/api/users/delete/"+email,
        type: "POST",
        datatype:"json",
        contentType: "application/json",
        success: function(data) {
            TableUsers.ajax.reload(null, false);
            }});


});

});