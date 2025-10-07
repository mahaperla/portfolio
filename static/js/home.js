// Home page specific JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize skill bar animations
    initSkillBars();
    
    // Initialize scroll animations
    initScrollAnimations();
    
    // Initialize typing effect
    initTypingEffect();
});

function initSkillBars() {
    const skillBars = document.querySelectorAll('.skill-progress');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const width = entry.target.getAttribute('data-width');
                setTimeout(() => {
                    entry.target.style.width = width;
                }, 300);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    skillBars.forEach(bar => {
        observer.observe(bar);
    });
}

function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

function initTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-effect');
    
    typingElements.forEach(element => {
        // Get the text and clean it
        let text = element.getAttribute('data-text');
        if (!text) return;
        
        // Clean the text thoroughly
        text = text.trim().replace(/\s+/g, ' '); // Replace multiple spaces with single space
        console.log('Original text from data-text:', text);
        
        // Clear any existing content and attributes
        element.textContent = '';
        element.removeAttribute('data-typed');
        
        // Set up the typing animation
        startTypingAnimation(element, text);
    });
}

function startTypingAnimation(element, text) {
    // Ensure element is clean
    element.textContent = '';
    
    let currentIndex = 0;
    
    function typeNextCharacter() {
        if (currentIndex < text.length) {
            const currentText = text.substring(0, currentIndex + 1);
            element.textContent = currentText;
            console.log(`Typing step ${currentIndex + 1}: "${currentText}"`);
            currentIndex++;
            setTimeout(typeNextCharacter, 100);
        } else {
            console.log('Typing completed:', element.textContent);
            // Mark as complete and remove cursor completely
            element.setAttribute('data-typed', 'true');
            element.style.borderRight = 'none';
            element.style.borderRightColor = 'transparent';
            element.style.borderRightWidth = '0';
            // Remove any animation classes and styles
            element.style.animation = 'none';
            element.style.animationName = 'none';
            element.classList.remove('typing-effect');
            // Force re-render
            element.offsetHeight;
        }
    }
    
    // Start typing after a short delay
    setTimeout(typeNextCharacter, 500);
}

// Removed old typeText function - using new startTypingAnimation instead