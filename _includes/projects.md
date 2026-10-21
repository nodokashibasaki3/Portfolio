<h2 id="projects" style="margin: 20px 0px 5px;">Selected Projects</h2>
<p style="color: #888; font-size: 0.85em; margin-bottom: 25px;">* Highlighted are ongoing projects.</p>
<style>
.project-container {
    display: flex;
    margin-bottom: 30px;
    align-items: center; /* Vertically center image relative to text */
}
.project-media {
    flex: 0 0 30%;
    max-width: 30%;
    padding-right: 15px;
    padding-left: 15px;
    position: relative;
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
        margin-left: 0 !important;
        margin-right: 0 !important;
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
    <div class="project-container" {% if project.ongoing %}style="background-color: rgba(255, 121, 0, 0.05); padding: 20px 60px 20px 20px; border-radius: 10px; margin-left: -20px; margin-right: -40px;"{% endif %}>
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
            {% else %}
                <div style="aspect-ratio: 4 / 3; display: flex; align-items: center; justify-content: center; border-radius: 4px; background-color: rgba(255, 121, 0, 0.08); color: #FF7900; font-size: 2em;">
                    <i class="fa-solid fa-lock" aria-label="Confidential project"></i>
                </div>
            {% endif %}
            {% if project.caption %}
                <p style="font-size: 0.75em; color: #888; margin: 4px 0 0 0; text-align: center; font-style: italic;">{{ project.caption }}</p>
            {% endif %}
        </div>
        <div class="project-content" style="flex: 0 0 70%; max-width: 70%; padding-right: 15px; padding-left: 20px;">
            <div class="title" style="font-weight: bolder; font-size: 1.1em;"><a style="color: inherit; text-decoration: none;">{{ project.title }}</a></div>
            <div class="author" style="margin-top: 2px;">{{ project.date }}{% if project.institution %} | {% if project.institution_url %}<a href="{{ project.institution_url }}" target="_blank" rel="noopener noreferrer">{{ project.institution }}</a>{% else %}{{ project.institution }}{% endif %}{% endif %}</div>
            <div class="periodical" style="margin-top: 5px; font-size: 0.95em;">{{ project.description }}</div>
            {% if project.paper %}
            <div class="paper" style="margin-top: 6px; font-size: 0.9em;"><i class="fa-regular fa-file-lines" style="margin-right: 4px;"></i>Published in <em>{{ project.paper.venue }}</em> · <a href="{{ project.paper.url }}" target="_blank" rel="noopener noreferrer">arXiv</a></div>
            {% endif %}
        </div>
    </div>
    {% endfor %}
</div>
