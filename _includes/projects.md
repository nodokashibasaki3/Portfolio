<h2 id="projects" style="margin: 20px 0px 10px;">Projects</h2>

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
.project-media video {
    width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 4px;
    background: transparent;
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
            {% if project.video %}
                <video width="100%" autoplay loop muted playsinline style="border-radius: 4px;">
                    {% assign file_ext = project.video | split: '.' | last | downcase %}
                    {% if file_ext == 'mov' %}
                        <source src="{{ project.video }}" type="video/quicktime">
                    {% elsif file_ext == 'webm' %}
                        <source src="{{ project.video }}" type="video/webm">
                    {% else %}
                        <source src="{{ project.video }}" type="video/mp4">
                    {% endif %}
                </video>
            {% elsif project.images %}
                <div class="project-images" style="display: flex; flex-direction: column; gap: 10px;">
                    {% for img in project.images %}
                        {% assign file_ext = img | split: '.' | last | downcase %}
                        {% if file_ext == 'mp4' or file_ext == 'mov' or file_ext == 'webm' %}
                            <video width="100%" autoplay loop muted playsinline style="border-radius: 4px;">
                                {% if file_ext == 'mov' %}
                                    <source src="{{ img }}" type="video/quicktime">
                                {% elsif file_ext == 'webm' %}
                                    <source src="{{ img }}" type="video/webm">
                                {% else %}
                                    <source src="{{ img }}" type="video/mp4">
                                {% endif %}
                            </video>
                        {% else %}
                            <img src="{{ img }}" alt="{{ project.title }}">
                        {% endif %}
                    {% endfor %}
                </div>
            {% elsif project.image %}
                {% assign file_ext = project.image | split: '.' | last | downcase %}
                {% if file_ext == 'mp4' or file_ext == 'mov' or file_ext == 'webm' %}
                    <video width="100%" autoplay loop muted playsinline style="border-radius: 4px;">
                        {% if file_ext == 'mov' %}
                            <source src="{{ project.image }}" type="video/quicktime">
                        {% elsif file_ext == 'webm' %}
                            <source src="{{ project.image }}" type="video/webm">
                        {% else %}
                            <source src="{{ project.image }}" type="video/mp4">
                        {% endif %}
                    </video>
                {% else %}
                    <img src="{{ project.image }}" alt="{{ project.title }}">
                {% endif %}
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
