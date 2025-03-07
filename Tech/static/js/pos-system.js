// Variables globales
let cart = []
let currentMode = "sale" // 'sale' o 'quote'
let currentQuoteData = null

// Función para inicializar la aplicación
document.addEventListener("DOMContentLoaded", () => {
  loadProducts()

  // Eventos de búsqueda y filtrado
  document.getElementById("searchProduct").addEventListener("input", debounce(loadProducts, 300))
  document.getElementById("categoryFilter").addEventListener("change", loadProducts)

  // Evento para completar la venta o crear cotización
  document.getElementById("completeSale").addEventListener("click", completeSale)

  // Evento para cambiar entre modo venta y cotización
  document.getElementById("toggleMode").addEventListener("click", toggleMode)

  // Inicializar el escáner de códigos de barras
  initBarcodeScanner()
})

// Función para cargar productos
function loadProducts() {
  const search = document.getElementById("searchProduct").value || ""
  const category = document.getElementById("categoryFilter").value || ""

  fetch(`/inventory/pos/products/?q=${search}&category=${category}`)
    .then((response) => response.json())
    .then((products) => {
      const grid = document.getElementById("productsGrid")
      grid.innerHTML = ""

      if (!products.length) {
        grid.innerHTML = '<p class="text-gray-500">No se encontraron productos</p>'
        return
      }

      products.forEach((product) => {
        const card = createProductCard(product)
        grid.appendChild(card)
      })
    })
    .catch((error) => console.error("Error cargando productos:", error))
}

// Función para crear una tarjeta de producto
function createProductCard(product) {
  const div = document.createElement("div")
  div.className = "product-card card p-2"

  if (product.stock <= 0) {
    div.classList.add("disabled")
  }

  div.onclick = () => {
    if (product.stock > 0) {
      addToCart(product)
    } else {
      alert("Producto agotado")
    }
  }

  div.innerHTML = `
        <img src="${product.image || "/static/img/no-image.png"}" 
             alt="${product.name}"
             class="w-full h-32 object-cover rounded mb-2">
        <h3 class="font-semibold truncate">${product.name}</h3>
        <p class="text-sm text-gray-600">${product.code}</p>
        <div class="flex justify-between items-center mt-2">
            <span class="font-bold">$${product.price}</span>
            <span class="text-sm ${product.stock < 5 ? "text-red-500" : "text-gray-600"}">
                Stock: ${product.stock > 0 ? product.stock : "Agotado"}
            </span>
        </div>
    `

  return div
}

// Función para agregar un producto al carrito
function addToCart(product) {
  if (product.stock <= 0) {
    alert("Producto agotado")
    return
  }

  const existingItem = cart.find((item) => item.product_id === product.id)

  if (existingItem) {
    if (existingItem.quantity >= product.stock) {
      alert("Stock insuficiente")
      return
    }
    existingItem.quantity++
  } else {
    cart.push({
      product_id: product.id,
      name: product.name,
      price: product.price,
      quantity: 1,
      stock: product.stock, // Añadimos el stock actual del producto
    })
  }

  updateCartDisplay()
}

// Función para actualizar la visualización del carrito
function updateCartDisplay() {
  const cartItems = document.getElementById("cartItems")
  cartItems.innerHTML = ""

  cart.forEach((item, index) => {
    const div = document.createElement("div")
    div.className = "cart-item"
    div.innerHTML = `
            <div class="flex-1">
                <h4 class="font-semibold">${item.name}</h4>
                <p class="text-sm text-gray-600">$${item.price} c/u</p>
            </div>
            <div class="quantity-controls">
                <button class="btn btn-sm btn-outline" onclick="updateQuantity(${index}, -1)">
                    <i class="fas fa-minus"></i>
                </button>
                <span class="mx-2">${item.quantity}</span>
                <button class="btn btn-sm btn-outline" onclick="updateQuantity(${index}, 1)">
                    <i class="fas fa-plus"></i>
                </button>
                <button class="btn btn-sm btn-outline text-red-500 ml-2" onclick="removeFromCart(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `
    cartItems.appendChild(div)
  })

  updateTotals()
}

// Función para actualizar la cantidad de un producto en el carrito
function updateQuantity(index, change) {
  const item = cart[index]
  const newQuantity = item.quantity + change

  if (newQuantity < 1) {
    removeFromCart(index)
    return
  }

  item.quantity = newQuantity
  updateCartDisplay()
}

// Función para eliminar un producto del carrito
function removeFromCart(index) {
  cart.splice(index, 1)
  updateCartDisplay()
}

// Función para actualizar los totales
function updateTotals() {
  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const tax = subtotal * 0.15
  const total = subtotal + tax

  document.getElementById("subtotal").textContent = `$${subtotal.toFixed(2)}`
  document.getElementById("tax").textContent = `$${tax.toFixed(2)}`
  document.getElementById("total").textContent = `$${total.toFixed(2)}`

  document.getElementById("completeSale").disabled = cart.length === 0
}

async function completeSale() {
    const completeSaleBtn = document.getElementById("completeSale");
  
    // Evita llamadas múltiples si ya está en proceso
    if (completeSaleBtn.disabled) return;
  
    completeSaleBtn.disabled = true;
    completeSaleBtn.textContent = "Procesando...";
  
    try {
      const customerName = document.getElementById("customerName").value.trim();
      const customerId = document.getElementById("customerId").value.trim();
      const paymentMethod = document.getElementById("paymentMethod").value;
      const notes = document.getElementById("saleNotes").value.trim();
  
      if (!cart.length || !cart.some((item) => item.quantity > 0)) {
        alert("El carrito está vacío o no contiene productos válidos.");
        return;
      }
  
      const data = {
        items: cart.map((item) => ({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price,
        })),
        customer_name: customerName,
        customer_id: customerId,
        payment_method: paymentMethod,
        notes: notes,
      };
  
      const endpoint = currentMode === "sale" ? "/pos/create-sale/" : "/pos/create-quote/";
  
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(data),
      });
  
      const responseData = await response.json();
  
      if (response.ok) {
        if (currentMode === "quote") {
          showQuoteModal(responseData);
        } else {
          showSaleModal(responseData);
        }
        resetCart();
      } else {
        throw new Error(responseData.error || "Error al procesar la solicitud");
      }
    } catch (error) {
      alert(error.message);
    } finally {
      completeSaleBtn.disabled = false;
      completeSaleBtn.textContent = currentMode === "sale" ? "Completar Venta" : "Crear Cotización";
    }
  }
  
// Función para mostrar el modal de venta
function showSaleModal(saleData) {
  const modal = document.getElementById("saleModal")
  const modalContent = modal.querySelector(".modal-content")

  modalContent.innerHTML = `
        <h3 class="text-lg font-semibold mb-4">Vista Previa de la Venta</h3>
        <div class="sale-preview mb-4">
            <p><strong>Venta #:</strong> ${saleData.sale_number}</p>
            <p><strong>Cliente:</strong> ${saleData.customer_name}</p>
            <p><strong>RUC/CI:</strong> ${saleData.customer_id}</p>
            <p><strong>Fecha:</strong> ${saleData.date}</p>
            <p><strong>Forma de Pago:</strong> ${saleData.payment_method}</p>
            
            <div class="items-table mt-4">
                <table class="w-full">
                    <thead>
                        <tr>
                            <th class="text-left">Producto</th>
                            <th class="text-right">Cant.</th>
                            <th class="text-right">Precio</th>
                            <th class="text-right">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${saleData.items
                          .map(
                            (item) => `
                            <tr>
                                <td>${item.name}</td>
                                <td class="text-right">${item.quantity}</td>
                                <td class="text-right">$${item.price}</td>
                                <td class="text-right">$${item.subtotal}</td>
                            </tr>
                        `,
                          )
                          .join("")}
                    </tbody>
                </table>
            </div>
            
            <div class="totals mt-4 text-right">
                <p><strong>Subtotal:</strong> $${saleData.subtotal}</p>
                <p><strong>IVA (15%):</strong> $${saleData.tax}</p>
                <p class="text-lg font-bold"><strong>Total:</strong> $${saleData.total}</p>
            </div>
        </div>
        <div class="flex justify-end gap-2 mt-4">
            <button class="btn btn-outline" onclick="printReceipt('${saleData.sale_number}')">
                <i class="fas fa-print mr-2"></i>
                Imprimir
            </button>
            <button class="btn btn-primary" onclick="closeSaleModal()">
                <i class="fas fa-check mr-2"></i>
                Aceptar
            </button>
        </div>
    `

  modal.style.display = "block"
}

// Función para mostrar el modal de cotización
function showQuoteModal(quoteData) {
  currentQuoteData = quoteData

  const modal = document.getElementById("quoteModal")
  const details = document.getElementById("quoteDetails")

  details.innerHTML = `
        <div class="quote-info">
            <p><strong>Cotización #:</strong> ${quoteData.quote_number}</p>
            <p><strong>Fecha:</strong> ${quoteData.date}</p>
            <p><strong>Cliente:</strong> ${quoteData.customer_name}</p>
            <p><strong>RUC/CI:</strong> ${quoteData.customer_id}</p>
        </div>
        <div class="quote-items">
            ${quoteData.items
              .map(
                (item) => `
                <div class="quote-item">
                    <span>${item.name} x${item.quantity}</span>
                    <span>$${item.subtotal}</span>
                </div>
            `,
              )
              .join("")}
        </div>
        <div class="quote-totals">
            <p>Subtotal: $${quoteData.subtotal}</p>
            <p>IVA (15%): $${quoteData.tax}</p>
            <p><strong>Total: $${quoteData.total}</strong></p>
        </div>
    `

  modal.style.display = "block"
}

// Función para imprimir recibo
function printReceipt(saleNumber) {
  window.open(`/pos/receipt/${saleNumber}/`, "_blank")
}

// Función para imprimir cotización
function printQuote(quoteNumber) {
  if (!currentQuoteData) {
    console.error("quoteData no está disponible")
    return
  }

  const url = `/pos/quote-pdf/${quoteNumber}/`
  console.log("Imprimiendo cotización desde:", url)
  window.open(url, "_blank")
}

// Función para convertir cotización a venta
function convertQuoteToSale(quoteNumber) {
  fetch(`/pos/quote-to-sale/${quoteNumber}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert(`Cotización convertida a Venta #${data.sale_number}`)
        closeQuoteModal()
        // Aquí podrías recargar la página o actualizar la UI según sea necesario
      } else {
        throw new Error(data.error)
      }
    })
    .catch((error) => {
      alert(error.message)
    })
}

// Función para cerrar el modal de venta
function closeSaleModal() {
  document.getElementById("saleModal").style.display = "none"
}

// Función para cerrar el modal de cotización
function closeQuoteModal() {
  document.getElementById("quoteModal").style.display = "none"
}

// Función para resetear el carrito
function resetCart() {
  cart = []
  updateCartDisplay()
  document.getElementById("customerName").value = ""
  document.getElementById("customerId").value = ""
  document.getElementById("saleNotes").value = ""
  document.getElementById("paymentMethod").value = "CASH"
}

// Función para cambiar entre modo venta y cotización
function toggleMode() {
  currentMode = currentMode === "sale" ? "quote" : "sale"
  const toggleBtn = document.getElementById("toggleMode")
  const completeSaleBtn = document.getElementById("completeSale")

  toggleBtn.textContent = currentMode === "sale" ? "Cambiar a Cotización" : "Cambiar a Venta"
  completeSaleBtn.textContent = currentMode === "sale" ? "Completar Venta" : "Crear Cotización"
}

// Función para inicializar el escáner de códigos de barras
function initBarcodeScanner() {
  let lastScannedCode = ""
  let scannerActive = false
  // Import ZXing library
  const codeReader = new ZXing.BrowserMultiFormatReader()

  document.getElementById("barcodeInput").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      const code = this.value.trim()
      if (code) {
        searchProductByCode(code)
        this.value = ""
      }
    }
  })

  document.getElementById("toggleCamera").addEventListener("click", () => {
    if (!scannerActive) {
      startCamera()
    } else {
      stopCamera()
    }
  })

  async function searchProductByCode(code) {
    try {
      // Asegurar que el código tenga exactamente 13 dígitos
      code = code.padStart(13, "0")

      const response = await fetch(`/pos/get-product/?code=${encodeURIComponent(code)}`)

      if (!response.ok) {
        const data = await response.json()
        if (data.error) {
          throw new Error(data.error)
        }
        throw new Error("Producto no encontrado")
      }

      const product = await response.json()
      showProductModal(product)
      addToCart(product)
    } catch (error) {
      alert(error.message)
      console.error("Error:", error)
    }
  }

  function showProductModal(product) {
    const modal = document.getElementById("productModal")

    document.getElementById("productImage").src = product.image || "/static/img/no-image.png"
    document.getElementById("productName").textContent = product.name
    document.getElementById("productPrice").textContent = `$${product.price}`
    document.getElementById("productStock").textContent = `Stock: ${product.stock}`
    document.getElementById("barcodeImage").src = product.barcode_image
    document.getElementById("barcodeNumber").textContent = product.barcode
    document.getElementById("qrCode").src = product.qr_code

    modal.style.display = "block"
  }

  async function startCamera() {
    try {
      const videoContainer = document.getElementById("videoContainer")
      const video = document.getElementById("video")

      videoContainer.style.display = "block"
      scannerActive = true

      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
      video.srcObject = stream
      video.play()

      codeReader.decodeFromVideoDevice(null, "video", (result, err) => {
        if (result && result.text !== lastScannedCode) {
          lastScannedCode = result.text
          searchProductByCode(result.text)
          stopCamera()
        }
      })
    } catch (error) {
      alert("Error al acceder a la cámara")
      console.error(error)
    }
  }

  function stopCamera() {
    const videoContainer = document.getElementById("videoContainer")
    const video = document.getElementById("video")

    if (video.srcObject) {
      video.srcObject.getTracks().forEach((track) => track.stop())
    }

    codeReader.reset()
    videoContainer.style.display = "none"
    scannerActive = false
  }
}

// Utilidad para obtener el token CSRF
function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Utilidad para debounce
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

