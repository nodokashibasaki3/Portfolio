<h2 id="projects" style="margin: 20px 0px 10px;">Research Projects</h2>

<style>
.project-container {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
    align-items: center; /* Vertically center image relative to text */
}
.project-media {
    flex: 0 0 180px;
}
.project-media img {
    width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 4px;
}
@media (max-width: 768px) {
    .project-container {
        flex-direction: column;
    }
    .project-media {
        flex: 0 0 auto;
        width: 100%;
        max-width: 400px; /* Limit width on mobile if needed */
    }
}
</style>

<div class="projects">
    {% for project in site.data.projects %}
    <div class="project-container">
        <div class="project-media">
            {% if project.images %}
                <div class="project-images" style="display: flex; flex-direction: column; gap: 10px;">
                    {% for img in project.images %}
                   <img src="{{ img }}" alt="{{ project.title }}">
                    {% endfor %}
                </div>
            {% else %}
                <img src="{{ project.image }}" alt="{{ project.title }}">
            {% endif %}
        </div>
        <div class="project-content" style="flex: 1;">
            <h3 style="margin-top: 0;">{{ project.title }}</h3>
            <p class="project-date" style="color: #666; font-size: 0.9em; margin-bottom: 10px;">{{ project.date }}</p>
            <p class="project-description">{{ project.description }}</p>
        </div>
    </div>
    {% endfor %}
</div>
