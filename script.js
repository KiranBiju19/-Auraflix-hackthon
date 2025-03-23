document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            // Toggle hamburger/close icon
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (navLinks && navLinks.classList.contains('active') && 
            !event.target.closest('.nav-links') && 
            !event.target.closest('.mobile-menu-btn')) {
            navLinks.classList.remove('active');
            // Reset hamburger icon
            const icon = mobileMenuBtn.querySelector('i');
            if (icon && icon.classList.contains('fa-times')) {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        }
    });
    
    // FAQ accordion functionality
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        question.addEventListener('click', () => {
            // Close all other open FAQ items
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                    // Reset plus icon
                    const icon = otherItem.querySelector('.faq-toggle i');
                    if (icon) {
                        icon.classList.remove('fa-minus');
                        icon.classList.add('fa-plus');
                    }
                }
            });
            
            // Toggle the current item
            item.classList.toggle('active');
            
            // Toggle plus/minus icon
            const icon = item.querySelector('.faq-toggle i');
            if (icon) {
                if (item.classList.contains('active')) {
                    icon.classList.remove('fa-plus');
                    icon.classList.add('fa-minus');
                } else {
                    icon.classList.remove('fa-minus');
                    icon.classList.add('fa-plus');
                }
            }
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    // Reset hamburger icon
                    const icon = mobileMenuBtn.querySelector('i');
                    if (icon && icon.classList.contains('fa-times')) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
        });
    });
    
    // Add animation to feature cards on scroll
    const featureCards = document.querySelectorAll('.feature-card');
    
    // Create an Intersection Observer
    const observeElements = (elements) => {
        const options = {
            threshold: 0.2
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, options);
        
        elements.forEach(element => {
            observer.observe(element);
        });
    };
    
    if (featureCards.length > 0) {
        // Add a class for initial state
        featureCards.forEach(card => {
            card.style.opacity = "0";
            card.style.transform = "translateY(20px)";
            card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        });
        
        // Initialize the observer
        observeElements(featureCards);
    }
    
    // Header background change on scroll
    const header = document.querySelector('header');
    const scrollThreshold = 100; // pixels from top
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Subtle parallax effect for hero section
    const heroContent = document.querySelector('.hero-content-wrapper');
    if (heroContent) {
        document.addEventListener('mousemove', (e) => {
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            const moveX = (x - 0.5) * 20;
            const moveY = (y - 0.5) * 20;
            
            heroContent.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
        });
    }
    
    // Popup for CTA and Learn More buttons
    const ctaButton = document.querySelector('.cta-button');
    const learnMoreButton = document.querySelector('.learn-more-button');
    
    const createModalPopup = (title) => {
        // Create modal elements
        const modalOverlay = document.createElement('div');
        modalOverlay.className = 'modal-overlay';
        modalOverlay.style.position = 'fixed';
        modalOverlay.style.top = '0';
        modalOverlay.style.left = '0';
        modalOverlay.style.width = '100%';
        modalOverlay.style.height = '100%';
        modalOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        modalOverlay.style.display = 'flex';
        modalOverlay.style.justifyContent = 'center';
        modalOverlay.style.alignItems = 'center';
        modalOverlay.style.zIndex = '1000';
        
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        modalContent.style.backgroundColor = 'white';
        modalContent.style.padding = '2rem';
        modalContent.style.borderRadius = '15px';
        modalContent.style.maxWidth = '500px';
        modalContent.style.textAlign = 'center';
        modalContent.style.position = 'relative';
        modalContent.style.animation = 'fadeInUp 0.5s ease forwards';
        
        const closeButton = document.createElement('span');
        closeButton.innerHTML = '&times;';
        closeButton.style.position = 'absolute';
        closeButton.style.top = '1rem';
        closeButton.style.right = '1.5rem';
        closeButton.style.fontSize = '1.8rem';
        closeButton.style.cursor = 'pointer';
        closeButton.style.color = '#666';
        
        const modalTitle = document.createElement('h3');
        modalTitle.textContent = title;
        modalTitle.style.marginBottom = '1.5rem';
        modalTitle.style.color = '#333';
        
        const modalText = document.createElement('p');
        modalText.textContent = 'Thank you for your interest! We are currently in beta. Leave your email to get early access to our platform.';
        modalText.style.marginBottom = '2rem';
        
        const emailForm = document.createElement('form');
        emailForm.innerHTML = `
            <div style="margin-bottom: 1.5rem;">
                <input type="email" placeholder="Your email address" required style="width: 100%; padding: 1rem; border-radius: 50px; border: 1px solid #ddd; font-family: 'Poppins', sans-serif; outline: none;">
            </div>
            <button type="submit" style="background: linear-gradient(to right, #ff0066, #ff3131); color: white; border: none; padding: 0.9rem 2rem; font-size: 1rem; font-weight: 600; border-radius: 50px; cursor: pointer; transition: all 0.3s ease; margin-top: 0.5rem; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 5px 15px rgba(255, 0, 102, 0.3);">Join Waitlist</button>
        `;
        
        // Append elements
        modalContent.appendChild(closeButton);
        modalContent.appendChild(modalTitle);
        modalContent.appendChild(modalText);
        modalContent.appendChild(emailForm);
        modalOverlay.appendChild(modalContent);
        document.body.appendChild(modalOverlay);
        
        // Handle close button
        closeButton.addEventListener('click', () => {
            document.body.removeChild(modalOverlay);
        });
        
        // Close modal when clicking outside
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                document.body.removeChild(modalOverlay);
            }
        });
        
        // Handle form submission
        emailForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = emailForm.querySelector('input[type="email"]').value;
            
            // Show success message
            modalContent.innerHTML = `
                <h3 style="margin-bottom: 1.5rem; color: #333;">Thank you!</h3>
                <p style="margin-bottom: 1rem;">We've added <strong>${email}</strong> to our waitlist.</p>
                <p>We'll notify you when we launch!</p>
                <button class="close-btn" style="background: linear-gradient(to right, #ff0066, #ff3131); color: white; border: none; padding: 0.9rem 2rem; font-size: 1rem; font-weight: 600; border-radius: 50px; cursor: pointer; transition: all 0.3s ease; margin-top: 1.5rem; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 5px 15px rgba(255, 0, 102, 0.3);">Close</button>
            `;
            
            // Handle close button
            modalContent.querySelector('.close-btn').addEventListener('click', () => {
                document.body.removeChild(modalOverlay);
            });
        });
    };
    
    if (ctaButton) {
        ctaButton.addEventListener('click', () => {
            createModalPopup('Get Started with SOCIO');
        });
    }
    
    if (learnMoreButton) {
        learnMoreButton.addEventListener('click', () => {
            createModalPopup('Learn More About SOCIO');
        });
    }
    
    // Initialize platform carousel
    const setupCarousel = () => {
        const carouselTrack = document.querySelector('.carousel-track');
        if (!carouselTrack) return;
        
        // Pause animation on hover
        carouselTrack.addEventListener('mouseenter', () => {
            carouselTrack.style.animationPlayState = 'paused';
        });
        
        carouselTrack.addEventListener('mouseleave', () => {
            carouselTrack.style.animationPlayState = 'running';
        });
    };
    
    setupCarousel();
});