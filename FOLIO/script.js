// ==========================================================================
// 6.1 THE DARK MODE TOGGLE INTERACTION
// ==========================================================================

// 1. Grab the toggle button from the HTML using its unique ID identifier
const themeToggleBtn = document.getElementById('theme-toggle');

// 2. Attach an event listener to run code whenever a user clicks the button
themeToggleBtn.addEventListener('click', () => {
    
    // 3. Toggle the '.dark' class on the body tag element
    document.body.classList.toggle('dark');
    
    // 4. Update the visual text emoji to match the user's active background state
    if (document.body.classList.contains('dark')) {
        themeToggleBtn.textContent = '☀️'; // Displays the sun when background is dark
    } else {
        themeToggleBtn.textContent = '🌙'; // Displays the moon when background is light
    }
});
// ==========================================================================
// PHASE 3: BACK TO TOP BUTTON ENGINE
// ==========================================================================

// 1. Grab the button element from the HTML document tree
const backToTopBtn = document.getElementById('back-to-top');

// 2. Listen to the global window container for scrolling activity
window.addEventListener('scroll', () => {
    
    // Check if the user has scrolled down more than 300 pixels from the top
    if (window.scrollY > 300) {
        // If true, inject the '.show' utility class to make it visible
        backToTopBtn.classList.add('show');
    } else {
        // If false (near the top), strip the class away to hide it
        backToTopBtn.classList.remove('show');
    }
});

// 3. Attach a click event listener directly to the button
backToTopBtn.addEventListener('click', () => {
    
    // Execute a native browser window scroll back to the coordinate point (0, 0)
    window.scrollTo({
        top: 0,
        behavior: 'smooth' // Forces the browser to glide up elegantly instead of flashing
    });
});
// ==========================================================================
// 6.2 THE SCROLL REVEAL TIMING ENGINE
// ==========================================================================

// 1. Establish structural visibility tracking configurations
const revealOptions = {
    root: null,          // Track intersection against the main viewport window
    threshold: 0.15,     // Fire the animation sequence when 15% of the item is seen
    rootMargin: "0px"    // Do not shift the boundaries of the viewport target box
};

// 2. Define the callback rules that manipulate the active elements
const revealCallback = (entries, observer) => {
    entries.forEach(entry => {
        // If an element crosses into view, change its styling state
        if (entry.isIntersecting) {
            entry.target.classList.add('active'); // Applies the active visibility styles
            observer.unobserve(entry.target);     // Unbind observation once animation fires
        }
    });
};

// 3. Instantiate your listener tool utilizing the parameters above
const revealObserver = new IntersectionObserver(revealCallback, revealOptions);

// 4. Gather every DOM layout object configured with your anchor keyword
const elementsToAnimate = document.querySelectorAll('.reveal');

// 5. Connect each discovered item directly to the viewing sensors
elementsToAnimate.forEach(element => {
    revealObserver.observe(element);
});
async function renderPortfolioProjects() {
    const projectsContainer = document.getElementById("projects-grid");
    if (!projectsContainer) return;

    try {
        // Fetch the compiled data file relative to the site path root
        const response = await fetch("projects.json");
        const projects = await response.json();

        // Clear out hardcoded static template mockups or loader loops
        projectsContainer.innerHTML = "";

        projects.forEach(project => {
            const card = document.createElement("div");
            card.className = "portfolio-card";
            
            card.innerHTML = `
                <div class="card-body">
                    <span class="badge">${project.primary_language}</span>
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div class="card-meta">
                        <span>⭐ ${project.stars_count}</span>
                        <span>🍴 ${project.forks_count}</span>
                    </div>
                    <div class="card-actions">
                        <a href="${project.html_url}" target="_blank" class="btn btn-secondary">Source Code</a>
                        ${project.homepage_live ? `<a href="${project.homepage_live}" target="_blank" class="btn btn-primary">Live Demo</a>` : ''}
                    </div>
                </div>
            `;
            projectsContainer.appendChild(card);
        });
    } catch (error) {
        console.error("Critical error parsing projects manifest array:", error);
        projectsContainer.innerHTML = `<p class="error-msg">Failed to load projects. Please try refreshing.</p>`;
    }
}

document.addEventListener("DOMContentLoaded", renderPortfolioProjects);
