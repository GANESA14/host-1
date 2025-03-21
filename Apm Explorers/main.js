const channelData = {
    name: "APM Explorerz",
    tagline: "Explore the world with Us",
    subscribeLink: "https://www.youtube.com/@APM_Explorers",
    about: "Join us on exciting bike rides as we explore beautiful places, hidden spots, and thrilling road trips. Every ride is a new adventure, from high mountains to scenic coastal roads. We love sharing these amazing experiences to inspire fellow cyclists to ride beyond their limits. Subscribe for epic rides, breathtaking views, and useful tips for your next cycling trip!",
    stats: [
        { number: 50, label: "Destinations Explored" },
        { number: 10000, label: "Total Kilometers" },
        { number: 50000, label: "Subscribers" }
    ],
    videos: [
        {
            id: "https://www.youtube.com/shorts/dE58L4lgx88",
            title: "Maaran Poratta Kadai 😁",
            description: "Exploring the stunning Rocky Mountain trails during sunset"
        },
        { 
            id: "https://www.youtube.com/shorts/eNEvKJbmVdM",
            title: "Gem of Tenkasi 😍",
            description: "Tirumalai murugan Kovil is gem of tenkasi "
        },
        {
            id: "https://www.youtube.com/shorts/qbFwqsRyx5Y",
            title: "Pablo Escober Edit 🥸",
            description: "Navigating through the concrete jungle on two wheels"
        },
        {
            id: "https://www.youtube.com/shorts/hlKet6Y8uTg",
            title: "Rugged Boys ah..🙀",
            description: "Gang oda orey fun thaa..."
        },
        {
            id: "https://www.youtube.com/shorts/4HkkBVreYgg",
            title: "Helmet Ethuku Namakku..😅",
            description: "Helmet laa , namakku theuvaiyaa"
        },
    ],
    testimonials: [
        {
            content: "APM Explorerz inspired me to take on my first major bike trip. The detailed guides and tips made planning so much easier!",
            name: "A.B Gaming",
            title: "Local Explorer",
            initial: "A"
        },
        {
            content: "I've been following this channel for years. The cinematography and storytelling are on another level. Every video feels like an adventure film.",
            name: "Savage King",
            title: "National Explorer",
            initial: "S"
        },
        {
            content: "The recommendations are spot on. I've purchased three items based on these reviews and they've all been perfect for my riding style.",
            name: "Subash",
            title: "Organizer",
            initial: "S"
        }
    ],
    gear: [
        {
            icon: "fa-bicycle",
            title: "Carbon Fiber Road Bike",
            description: "Ourtrusty companion for long-distance journeys and city exploration"
        },
        {
            icon: "fa-camera",
            title: "Adventure Camera",
            description: "Waterproof, shockproof, and perfect for capturing trail moments"
        },
        {
            icon: "fa-compass",
            title: "GPS Navigation System",
            description: "Never get lost with this reliable backcountry navigator"
        },
       
    ],
    socialLinks: {
        Instagram: "https://www.instagram.com/apm_explorers_",
        YouTube: "https://www.youtube.com/@APM_Explorers",
        TikTok: "https://www.tiktok.com/@APMExplorerz",
        github:'https://github.com/GANESA14'
    }
};
document.getElementById("channel-name").textContent = channelData.name;
document.getElementById("channel-tagline").textContent = channelData.tagline;
document.getElementById("subscribe-link").href = channelData.subscribeLink;
document.getElementById("about-text").textContent = channelData.about;
const statsContainer = document.getElementById("stats-container");
channelData.stats.forEach(stat => {
    const statItem = document.createElement("div");
    statItem.className = "stat-item animate__animated";
    statItem.innerHTML = `
        <div class="stat-number" data-count="${stat.number}">0</div>
        <div class="stat-label">${stat.label}</div>
    `;
    statsContainer.appendChild(statItem);
});
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-count'));
        const duration = 2000;
        const increment = Math.ceil(target / (duration / 20)); 
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current > target) current = target;
            stat.textContent = current.toLocaleString();
            if (current < target) {
                setTimeout(updateCounter, 20);
            }
        };
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.disconnect();
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(stat);
    });
}
const videoContainer = document.getElementById("video-container");
channelData.videos.forEach((video, index) => {
    const videoCard = document.createElement("div");
    videoCard.className = "video-card";
    const videoId = video.id.split("/shorts/")[1];
    videoCard.innerHTML = `
         <iframe src="https://www.youtube.com/embed/${videoId}" allowfullscreen></iframe>
  
        <div class="video-info">
            <h3>${video.title}</h3>
            <p>${video.description}</p>
            </div>
    `;
    videoContainer.appendChild(videoCard);
    setTimeout(() => {
        videoCard.classList.add('animated');
    }, 100 * index);
});
const testimonialContainer = document.getElementById("testimonial-container");
channelData.testimonials.forEach((testimonial, index) => {
    const testimonialCard = document.createElement("div");
    testimonialCard.className = "testimonial-card";
    testimonialCard.innerHTML = `
        <div class="testimonial-content">${testimonial.content}</div>
        <div class="testimonial-author">
            <div class="author-avatar">${testimonial.initial}</div>
            <div class="author-info">
                <div class="author-name">${testimonial.name}</div>
                <div class="author-title">${testimonial.title}</div>
            </div>
        </div>
    `;
    testimonialContainer.appendChild(testimonialCard);
    setTimeout(() => {
        testimonialCard.classList.add('animated');
    }, 100 * index);
});
const gearContainer = document.getElementById("gear-container");
channelData.gear.forEach((item, index) => {
    const gearCard = document.createElement("div");
    gearCard.className = "gear-card";
    gearCard.innerHTML = `
        <div class="gear-image">
            <i class="fas ${item.icon}"></i>
        </div>
        <div class="gear-info">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
        </div>
    `;
    gearContainer.appendChild(gearCard);
    setTimeout(() => {
        gearCard.classList.add('animated');
    }, 100 * index);
});
const socialLinks = document.getElementById("social-links");
for (const [platform, url] of Object.entries(channelData.socialLinks)) {
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.innerHTML = `<i class="fab fa-${platform.toLowerCase()}"></i>`;
    socialLinks.appendChild(link);
}
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate__fadeInUp');
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.animate__animated').forEach(el => {
    observer.observe(el);
});
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.nav-bar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});
document.addEventListener('DOMContentLoaded', () => {
    animateStats();
    document.getElementById('newsletter-form').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thanks for subscribing! You will receive updates on future adventures.');
        this.reset();
    });
});
