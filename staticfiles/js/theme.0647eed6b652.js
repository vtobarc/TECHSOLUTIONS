document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
  
    // Theme toggle functionality
    const toggleTheme = () => {
      body.classList.toggle('dark-mode');
      localStorage.setItem('theme', body.classList.contains('dark-mode') ? 'dark' : 'light');
    };
  
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      body.classList.add('dark-mode');
    }
  
    // Add theme toggle button if it doesn't exist
    if (!themeToggle) {
      const newThemeToggle = document.createElement('button');
      newThemeToggle.id = 'theme-toggle';
      newThemeToggle.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9z"/>
        </svg>
      `;
      newThemeToggle.classList.add('theme-toggle');
      document.querySelector('.navigation').appendChild(newThemeToggle);
      
      newThemeToggle.addEventListener('click', toggleTheme);
    } else {
      themeToggle.addEventListener('click', toggleTheme);
    }
  
    // Dropdown and Menu Toggle Interactions
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    const navMenu = document.getElementById('nav-menu');
    const menuToggle = document.getElementById('menu-toggle');
    const overlay = document.getElementById('overlay');
  
    // Profile Dropdown Toggle
    if (profileBtn && profileDropdown) {
      profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdown.classList.toggle('show');
        overlay.classList.toggle('show');
      });
    }
  
    // Mobile Menu Toggle
    if (menuToggle && navMenu) {
      menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
        overlay.classList.toggle('show');
      });
    }
  
    // Close dropdowns when clicking outside
    document.addEventListener('click', (e) => {
      if (profileDropdown && !profileDropdown.contains(e.target) && 
          profileBtn && !profileBtn.contains(e.target)) {
        profileDropdown.classList.remove('show');
      }
      
      if (navMenu && !navMenu.contains(e.target) && 
          menuToggle && !menuToggle.contains(e.target)) {
        navMenu.classList.remove('show');
      }
      
      overlay.classList.remove('show');
    });
  
    // Notification and Message Dropdown Interactions
    const notificationIcon = document.querySelector('.notification-icon');
    const messageIcon = document.querySelector('.message-icon');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    const messagesDropdown = document.getElementById('messages-dropdown');
  
    if (notificationIcon && notificationsDropdown) {
      notificationIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        notificationsDropdown.classList.toggle('show');
        overlay.classList.toggle('show');
      });
    }
  
    if (messageIcon && messagesDropdown) {
      messageIcon.addEventListener('click', (e) => {
        e.stopPropagation();
        messagesDropdown.classList.toggle('show');
        overlay.classList.toggle('show');
      });
    }
  });