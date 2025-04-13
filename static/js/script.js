document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('loginModal');
    const loginBtn = document.getElementById('login-btn');
    const closeBtn = document.querySelector('.close');
    const getStartedBtn = document.getElementById('get-started-btn');
    
    // Open modal
    loginBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });
    
    // Another button to open modal
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', function() {
            modal.style.display = 'block';
        });
    }
    
    // Close modal
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // Account for fixed header
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            // Simple validation
            if (!name || !email || !message) {
                alert('Please fill out all fields');
                return;
            }
            
            // In a real application, you would send this data to your server
            // For this simulation, we'll just show a success message
            alert(`Thank you for your message, ${name}! We'll get back to you soon.`);
            
            // Clear the form
            contactForm.reset();
        });
    }
    
    // Flash messages auto-dismiss
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });
    
    // Code to handle active navigation highlighting
    function setActiveNavItem() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
        
        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (scrollY >= (sectionTop - 200)) {
                    current = section.getAttribute('id');
                }
            });
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }
    
    // Transaction Flow Animation - Auto Play
    const transactionContainer = document.querySelector('.transaction-animation-container');
    if (transactionContainer) {
        const transactionSteps = [
            {
                step: 1,
                description: "Step 1: Party A initiates transaction and sends money to escrow.",
                action: function() {
                    // Reset everything to initial state
                    document.querySelector('.arrow-a-to-escrow').classList.remove('animate-transfer');
                    document.querySelector('.arrow-escrow-to-b').classList.remove('animate-transfer');
                    document.querySelector('.arrow-a-to-escrow .transfer-amount').style.opacity = '0';
                    document.querySelector('.arrow-escrow-to-b .transfer-amount').style.opacity = '0';
                    
                    // Set initial balances
                    document.querySelector('.party-a .actor-money').textContent = '$500';
                    document.querySelector('.escrow .actor-money').textContent = '$0';
                    document.querySelector('.party-b .actor-money').textContent = '$200';
                    
                    // Add animation class to first arrow after a brief delay
                    setTimeout(function() {
                        document.querySelector('.arrow-a-to-escrow').classList.add('animate-transfer');
                        document.querySelector('.arrow-a-to-escrow .transfer-amount').style.opacity = '1';
                    }, 500);
                }
            },
            {
                step: 2,
                description: "Step 2: Party B delivers the service or product as agreed.",
                action: function() {
                    // Update balances to reflect money in escrow
                    document.querySelector('.party-a .actor-money').textContent = '$400';
                    document.querySelector('.escrow .actor-money').textContent = '$100';
                    document.querySelector('.party-b .actor-money').textContent = '$200';
                }
            },
            {
                step: 3,
                description: "Step 3: Party B marks the service as completed in the system.",
                action: function() {
                    // First arrow complete, no changes to balances in this step
                    // Visual cue that we're preparing for next step
                    document.querySelector('.arrow-a-to-escrow').classList.remove('animate-transfer');
                    document.querySelector('.arrow-a-to-escrow .transfer-amount').style.opacity = '0';
                }
            },
            {
                step: 4,
                description: "Step 4: Party A confirms completion and funds are released to Party B.",
                action: function() {
                    // Add animation to second arrow
                    document.querySelector('.arrow-escrow-to-b').classList.add('animate-transfer');
                    document.querySelector('.arrow-escrow-to-b .transfer-amount').style.opacity = '1';
                    
                    // After a delay, update the balances
                    setTimeout(function() {
                        document.querySelector('.escrow .actor-money').textContent = '$0';
                        document.querySelector('.party-b .actor-money').textContent = '$300';
                    }, 1500);
                }
            }
        ];
        
        let currentStepIndex = 0;
        const stepDelay = 3000; // 3 seconds between steps
        
        // Function to play a single animation step
        function playAnimationStep() {
            // Get current step
            const currentStep = transactionSteps[currentStepIndex];
            
            // Update step indicator if it exists
            const stepIndicator = document.getElementById('currentStep');
            if (stepIndicator) {
                stepIndicator.textContent = `Step ${currentStep.step}/4`;
            }
            
            // Update description if it exists
            const descriptionElement = document.getElementById('stepDescription');
            if (descriptionElement) {
                descriptionElement.textContent = currentStep.description;
            }
            
            // Execute animation action
            currentStep.action();
            
            // Advance to next step after delay
            currentStepIndex++;
            
            // Schedule next step or reset animation
            if (currentStepIndex < transactionSteps.length) {
                setTimeout(playAnimationStep, stepDelay);
            } else {
                // Reset after completing all steps and a longer delay
                currentStepIndex = 0;
                setTimeout(playAnimationStep, stepDelay + 1000);
            }
        }
        
        // Function to check if element is in viewport
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }
        
        // Start the animation when in viewport
        function checkAndStartAnimation() {
            if (!window.animationStarted && isInViewport(transactionContainer)) {
                window.animationStarted = true;
                playAnimationStep();
            }
        }
        
        // Check on load and scroll events
        window.addEventListener('scroll', checkAndStartAnimation);
        window.addEventListener('load', checkAndStartAnimation);
        
        // Also start animation when getting close to the animation
        window.addEventListener('scroll', function() {
            if (!window.animationStarted) {
                const rect = transactionContainer.getBoundingClientRect();
                if (rect.top < window.innerHeight + 200) { // Start when getting close
                    window.animationStarted = true;
                    playAnimationStep();
                }
            }
        });
        
        // Initial check to start animation if already visible
        checkAndStartAnimation();
    }
    
    setActiveNavItem();
});