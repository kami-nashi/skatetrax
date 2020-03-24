// Call the dataTables jQuery plugin
//$(document).ready(function() {
//  $('#dataTable').DataTable();
//});

$.getJSON(apiUrl_sessions, function(jsonFromFile) {
  $('#dataTable').bootstrapTable({
    data: jsonFromFile,
    "pagingType": "full_numbers"
  });
   $('.dataTables_length').addClass('bs-select');
});

