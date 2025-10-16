// Animation script
document.addEventListener("DOMContentLoaded", function() {
    console.log("Animation script loaded");
    
    // Hide leadership experiences by default
    const leadershipItems = document.querySelectorAll('.timeline-item[data-category="leadership"]');
    leadershipItems.forEach(item => {
        item.classList.add('hidden');
    });
    
    // Define emoji set for floating particles
    const emojis = ["💻", "🤖", "🧠", "⚡", "🔬", "🚀", "🔋", "🛠️", "🧮", "🧪"];
    
    // Create floating emoji particles
    function createParticle() {
        const particle = document.createElement('div');
        particle.classList.add('emoji-particle');
        
        // Random emoji
        const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
        particle.textContent = randomEmoji;
        
        // Random position
        const startX = Math.random() * 100;
        
        // Set styles
        particle.style.left = `${startX}%`;
        particle.style.animationDuration = `${8 + Math.random() * 12}s`;
        particle.style.animationDelay = `${Math.random() * 2}s`;
        
        // Append to body
        document.body.appendChild(particle);
        
        // Remove after animation
        setTimeout(() => {
            particle.remove();
        }, 20000);
    }
    
    // Create initial particles
    for (let i = 0; i < 8; i++) {
        setTimeout(createParticle, i * 300);
    }
    
    // Create particles periodically
    setInterval(createParticle, 2000);
        
    // Add profile pic interaction
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
                    
                    // Position around the image
                    const angle = (index * 120) * (Math.PI / 180);
                    const radius = 80;
                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;
                    
                    // Get the position relative to the viewport
                    const rect = this.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    
                    // Position the emoji relative to center of profile pic
                    reaction.style.position = 'fixed';
                    reaction.style.top = `${centerY + y}px`;
                    reaction.style.left = `${centerX + x}px`;
                    
                    document.body.appendChild(reaction);
                    
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
            
            // Get the position relative to the viewport
            const rect = this.getBoundingClientRect();
            
            // Position the indicator above the tech span
            indicator.style.position = 'fixed';
            indicator.style.top = `${rect.top - 20}px`;
            indicator.style.left = `${rect.left + rect.width / 2}px`;
            
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

// Experience Slider Animation
document.addEventListener('DOMContentLoaded', () => {
    const list = document.getElementById('experience-list');
    if (!list) return; // Exit if the element doesn't exist

    const items = Array.from(list.children);
    const itemHeight = 50;
    const visibleCenterIndex = Math.floor(300 / itemHeight / 2);
    let focusIndex = Math.floor(items.length / 2);

    // Update data-type attributes to be more descriptive
    items.forEach(item => {
        const type = item.getAttribute('data-type');
        if (type === 'leadership') {
            item.setAttribute('data-type', 'Leadership');
        } else if (type === 'engineering') {
            item.setAttribute('data-type', 'Engineering');
        } else if (type === 'life') {
            item.setAttribute('data-type', 'Life Transition');
        }
    });
    
    // -[X] you finished this

    function updateFocus(newIndex) {
        items.forEach((item, i) => {
            item.classList.toggle('focused', i === newIndex);
        });

        const offset = (300 / 2) - (newIndex * itemHeight + itemHeight / 2);
        list.style.transform = `translateY(${offset}px)`;
        focusIndex = newIndex;
    }

    items.forEach((item, index) => {
        item.addEventListener('click', () => {
            updateFocus(index);
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' && focusIndex < items.length - 1) {
            updateFocus(focusIndex + 1);
        }
        if (e.key === 'ArrowUp' && focusIndex > 0) {
            updateFocus(focusIndex - 1);
        }
    });

    updateFocus(focusIndex);
});

function toggleLeadership() {
    const leadershipItems = document.querySelectorAll('.timeline-item[data-category="leadership"]');
    const toggleButton = document.getElementById('leadership-toggle');
    
    // Check if leadership items are currently hidden
    const isHidden = leadershipItems[0]?.classList.contains('hidden');
    
    if (isHidden) {
        // Show leadership items
        leadershipItems.forEach(item => {
            item.classList.remove('hidden');
        });
        toggleButton.textContent = 'Hide Leadership';
        toggleButton.classList.add('active');
    } else {
        // Hide leadership items
        leadershipItems.forEach(item => {
            item.classList.add('hidden');
        });
        toggleButton.textContent = 'Show Leadership';
        toggleButton.classList.remove('active');
    }
} 