// Particle animation for the header
document.addEventListener("DOMContentLoaded", function() {
    const emojis = ["💻", "🤖", "🧠", "⚡", "🔬", "🚀", "🔋", "🛠️", "🧮", "🧪"];
    const profileContainer = document.querySelector('.profile-container');
    
    // Create floating emoji particles
    function createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('emoji-particle');
        
        // Random emoji
        const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
        particle.textContent = randomEmoji;
        
        // Random position
        const startX = Math.random() * 100;
        const startOpacity = 0.1 + Math.random() * 0.5;
        
        // Set styles
        particle.style.left = `${startX}%`;
        particle.style.opacity = startOpacity;
        particle.style.animationDuration = `${8 + Math.random() * 12}s`;
        particle.style.animationDelay = `${Math.random() * 5}s`;
        
        // Append to container
        document.body.appendChild(particle);
        
        // Remove after animation
        setTimeout(() => {
            particle.remove();
        }, 20000);
    }
    
    // Create particles periodically
    setInterval(createParticle, 2000);
    
    // Create initial particles
    for (let i = 0; i < 8; i++) {
        setTimeout(createParticle, i * 300);
    }
    
    // Project card hover effects
    const projectCards = document.querySelectorAll('.project-container, .mini-project');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const emoji = document.createElement('div');
            emoji.classList.add('reaction-emoji');
            emoji.textContent = "✨";
            this.appendChild(emoji);
            
            setTimeout(() => {
                emoji.remove();
            }, 1000);
        });
    });
    
    // Add typing effect to the main title
    const title = document.querySelector('h1');
    const originalText = title.textContent;
    title.textContent = '';
    
    let i = 0;
    const typeTitle = setInterval(() => {
        if (i < originalText.length) {
            title.textContent += originalText.charAt(i);
            i++;
        } else {
            clearInterval(typeTitle);
            // Add blinking cursor at the end
            const cursor = document.createElement('span');
            cursor.classList.add('typing-cursor');
            cursor.textContent = '|';
            title.appendChild(cursor);
            
            // Remove cursor after a few seconds
            setTimeout(() => {
                cursor.remove();
            }, 3000);
        }
    }, 100);
    
    // Add interactive effect for profile pic
    const profilePic = document.getElementById('profile-pic');
    
    if (profilePic) {
        profilePic.addEventListener('mouseenter', function() {
            this.style.transition = 'transform 0.5s ease';
            this.style.transform = 'scale(1.05)';
            
            // Create emoji reactions around profile
            const reactions = ["🔋", "🧠", "🚀"];
            
            reactions.forEach((emoji, index) => {
                setTimeout(() => {
                    const reaction = document.createElement('div');
                    reaction.classList.add('profile-reaction');
                    reaction.textContent = emoji;
                    reaction.style.animationDelay = `${index * 0.2}s`;
                    
                    // Position around the image
                    const angle = (index * 120) * (Math.PI / 180);
                    const radius = 80;
                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;
                    
                    reaction.style.left = `calc(50% + ${x}px)`;
                    reaction.style.top = `calc(50% + ${y}px)`;
                    
                    this.parentElement.appendChild(reaction);
                    
                    setTimeout(() => {
                        reaction.remove();
                    }, 1500);
                }, index * 200);
            });
        });
        
        profilePic.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    }
    
    // Tech stack hover effect
    const techSpans = document.querySelectorAll('.tech-stack span');
    techSpans.forEach(span => {
        span.addEventListener('mouseenter', function() {
            this.classList.add('tech-hover');
            
            // Create a small emoji indicator
            const indicator = document.createElement('div');
            indicator.classList.add('tech-indicator');
            indicator.textContent = "🔍";
            indicator.style.top = `${this.offsetTop - 20}px`;
            indicator.style.left = `${this.offsetLeft + this.offsetWidth / 2}px`;
            document.body.appendChild(indicator);
            
            setTimeout(() => {
                indicator.remove();
            }, 1000);
        });
        
        span.addEventListener('mouseleave', function() {
            this.classList.remove('tech-hover');
        });
    });
});