$(document).ready(function(){
    const url = '/api/invoices';


tableInvoices=$('#invoicesTable').DataTable({
        ajax:{
            url:url,
            dataSrc:''
        },
        columns:[
            {data: "Num_invoices"},
            {data: "Date_invoices"},
            {data: "Origin_invoices"},
            {data: "Total_invoices"},
            {data: "RFC_clients"},
            {data: null,
                render: function ( data, type, row ) {
                  return '<button x-on:click="isModalOpen = true"  class="text-base btnEdit  rounded-l-none rounded-r-none border-l-0 border-r-0  hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer hover:bg-teal-700  hover:text-green-400 bg-teal-100 text-teal-700 border duration-200 ease-in-out border-teal-600 transition"><div class="flex leading-5"><svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit w-5 h-5 mr-1"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>   </svg>   Edit</div>  </button> <button BtnDelete x-on:click="isConfirm = true" class="text-base  rounded-l-none rounded-r-none border-l-0 border-r-0  hover:scale-110 focus:outline-none flex justify-center px-4 py-2 rounded font-bold cursor-pointer hover:bg-red-4000 hover:text-red-500 bg-teal-100 text-teal-700 border duration-200 ease-in-out border-teal-600 transition"><div class="flex leading-5"><svg class="svg-icon" viewBox="0 0 20 20"><path d="M17.114,3.923h-4.589V2.427c0-0.252-0.207-0.459-0.46-0.459H7.935c-0.252,0-0.459,0.207-0.459,0.459v1.496h-4.59c-0.252,0-0.459,0.205-0.459,0.459c0,0.252,0.207,0.459,0.459,0.459h1.51v12.732c0,0.252,0.207,0.459,0.459,0.459h10.29c0.254,0,0.459-0.207,0.459-0.459V4.841h1.511c0.252,0,0.459-0.207,0.459-0.459C17.573,4.127,17.366,3.923,17.114,3.923M8.394,2.886h3.214v0.918H8.394V2.886z M14.686,17.114H5.314V4.841h9.372V17.114z M12.525,7.306v7.344c0,0.252-0.207,0.459-0.46,0.459s-0.458-0.207-0.458-0.459V7.306c0-0.254,0.205-0.459,0.458-0.459S12.525,7.051,12.525,7.306M8.394,7.306v7.344c0,0.252-0.207,0.459-0.459,0.459s-0.459-0.207-0.459-0.459V7.306c0-0.254,0.207-0.459,0.459-0.459S8.394,7.051,8.394,7.306"></path></svg>Erase</div> </button>'; }},
        ],
        responsive: true
    });

var row; 
$(document).on("click", ".btnEdit", function(){	
    $("#invoicesTable").trigger("reset");
    row = $(this).closest("tr");	        
    Num_invoices = row.find('td:eq(0)').text();
    Date_invoices = row.find('td:eq(1)').text();
    Origin_invoices = row.find('td:eq(2)').text();
    Total_invoices = row.find('td:eq(3)').text();
    RFC_clients = row.find('td:eq(4)').text();
    $("#Num_invoices").val(Num_invoices);
    $("#Date_invoices").val(Date_invoices);
    $("#Origin_invoices").val(Origin_invoices);
    $("#Total_invoices").val(Total_invoices);
    $("#RFC_clients").val(RFC_clients);

    


});


$('#formsUpdate').submit(function(e){                         
    e.preventDefault(); //evita el comportambiento normal del submit, es decir, recarga total de la página
    Num_invoices = $("#Num_invoices").val();
    Date_invoices = $("#Date_invoices").val();
    Origin_invoices = $("#Origin_invoices").val();
    Total_invoices = $("#Total_invoices").val();
    RFC_clients = $("#RFC_clients").val();
    var invoices = {
        Num_invoices: Num_invoices,
        Date_invoices: Date_invoices,
        Origin_invoices: Origin_invoices,
        Total_invoices: Total_invoices,
        RFC_clients: RFC_clients
    };
    var json = JSON.stringify(invoices);

        $.ajax({
          url: "/api/invoices/update/"+Num_invoices,
          type: "POST",
          datatype:"json",    
          contentType: "application/json",
          data: json,
          success: function(data) {
            tableInvoices.ajax.reload(null, false);
           }
           
        });			        
});
$('#tableDelete').submit(function(e){
    e.preventDefault(); 
    row = $(this).closest("tr");	        
    
    Num_invoice= parseInt(row.find('td:eq(0)').text()); //capturo el ID

    $.ajax({
        url: "/api/invoice/delete/"+Num_invoice,
        type: "POST",
        datatype:"json",
        contentType: "application/json",
        success: function(data) {
            tableInvoices.ajax.reload(null, false);
            }});


});

});