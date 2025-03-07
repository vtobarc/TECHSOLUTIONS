// Toggle Sidebar
document.addEventListener('DOMContentLoaded', function() {
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Inicializar DataTables si existe
    if ($.fn.DataTable && document.querySelector('table.dataTable')) {
        $('table.dataTable').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json'
            }
        });
    }
    
    // Inicializar Select2 si existe
    if ($.fn.select2 && document.querySelector('.select2')) {
        $('.select2').select2();
    }
    
    // Inicializar DatePicker si existe
    if ($.fn.datepicker && document.querySelector('.datepicker')) {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            language: 'es',
            autoclose: true
        });
    }
});