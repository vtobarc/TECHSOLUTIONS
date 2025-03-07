// static/js/inventory.js
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const toggleBtn = document.getElementById('toggleSidebar');
    const sidebar = document.getElementById('sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Search functionality
    const searchInput = document.querySelector('.search-bar input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Barcode Modal
    const modal = document.getElementById('barcodeModal');
    const closeBtn = document.querySelector('.close');
    const barcodeImage = document.getElementById('barcodeImage');

    window.showBarcode = function(imageUrl) {
        modal.style.display = 'block';
        barcodeImage.src = imageUrl;
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Print Barcode
    window.printBarcode = function() {
        const printWindow = window.open('', '', 'width=600,height=600');
        printWindow.document.write('<html><head><title>Print Barcode</title>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<img src="' + barcodeImage.src + '" style="width: 100%;">');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    }

    // Delete confirmation
    window.confirmDelete = function(productId) {
        if (confirm('¿Está seguro de que desea eliminar este producto?')) {
            window.location.href = `/inventory/product/${productId}/delete/`;
        }
    }

    // File input preview
    const imageInput = document.querySelector('input[type="file"]');
    const imagePreview = document.querySelector('.image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }
});