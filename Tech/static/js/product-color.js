// Save this in a file like static/js/product-color.js
document.addEventListener('DOMContentLoaded', function() {
    // Find all color circles on the page
    const colorCircles = document.querySelectorAll('.color-circle');
    
    colorCircles.forEach(circle => {
      const colorText = circle.nextElementSibling.textContent.trim();
      
      // Ensure the color is properly applied
      applyColorToCircle(circle, colorText);
      
      // Optional: Add click functionality to toggle between color formats
      circle.addEventListener('click', function() {
        toggleColorFormat(circle, colorText);
      });
    });
  });
  
  /**
   * Ensures the color is properly applied to the circle
   * @param {HTMLElement} circle - The color circle element
   * @param {string} colorValue - The color value from the database
   */
  function applyColorToCircle(circle, colorValue) {
    // If the color is already set via inline style, we don't need to do anything
    if (circle.style.backgroundColor) return;
    
    // Handle named colors, hex codes, and RGB values
    if (isValidColor(colorValue)) {
      circle.style.backgroundColor = colorValue;
    } else {
      // Fallback to a default color if the value isn't a valid CSS color
      circle.style.backgroundColor = '#CCCCCC';
      
      // Add a title attribute to explain why the color might not be showing correctly
      circle.title = `Unable to display color: ${colorValue}`;
    }
  }
  
  /**
   * Checks if a string is a valid CSS color value
   * @param {string} color - The color to validate
   * @returns {boolean} - Whether the color is valid
   */
  function isValidColor(color) {
    // Create a temporary element to test the color
    const testElem = document.createElement('div');
    testElem.style.color = color;
    
    // If the color is invalid, the browser will ignore it and this will be empty
    return !!testElem.style.color;
  }
  
  /**
   * Optional: Toggle between different formats of the same color
   * @param {HTMLElement} circle - The color circle element
   * @param {string} originalColor - The original color value
   */
  function toggleColorFormat(circle, originalColor) {
    // Get the current display format
    const currentFormat = circle.dataset.format || 'original';
    const nextSibling = circle.nextElementSibling;
    
    // Create a temporary element to get computed color
    const tempElement = document.createElement('div');
    tempElement.style.color = originalColor;
    document.body.appendChild(tempElement);
    const computedColor = getComputedStyle(tempElement).color;
    document.body.removeChild(tempElement);
    
    // Parse the RGB values
    const rgbMatch = computedColor.match(/rgb$$(\d+),\s*(\d+),\s*(\d+)$$/);
    if (!rgbMatch) return;
    
    const [_, r, g, b] = rgbMatch.map(Number);
    
    // Toggle between formats
    let newDisplay;
    let newFormat;
    
    switch(currentFormat) {
      case 'original':
        // Convert to hex
        newDisplay = rgbToHex(r, g, b);
        newFormat = 'hex';
        break;
      case 'hex':
        // Convert to RGB
        newDisplay = `rgb(${r}, ${g}, ${b})`;
        newFormat = 'rgb';
        break;
      case 'rgb':
        // Back to original
        newDisplay = originalColor;
        newFormat = 'original';
        break;
      default:
        newDisplay = originalColor;
        newFormat = 'original';
    }
    
    // Update the display
    if (nextSibling) {
      nextSibling.textContent = newDisplay;
    }
    
    // Store the current format
    circle.dataset.format = newFormat;
  }
  
  /**
   * Convert RGB values to hex color code
   * @param {number} r - Red value (0-255)
   * @param {number} g - Green value (0-255)
   * @param {number} b - Blue value (0-255)
   * @returns {string} - Hex color code
   */
  function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => {
      const hex = x.toString(16);
      return hex.length === 1 ? '0' + hex : hex;
    }).join('');
  }