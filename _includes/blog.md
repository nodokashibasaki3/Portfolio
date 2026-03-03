<h2 id="blog" style="margin: 60px 0px 15px;">Blog</h2>

<div class="blog-container" style="display: flex; flex-direction: column; gap: 10px;">
    {% for post in site.data.blog %}
    <div class="blog-post" style="display: flex; align-items: baseline; font-size: 0.95em;">
        {% if post.date %}
        <div class="date" style="color: #999; width: 60px; flex-shrink: 0; font-size: 0.9em;">{{ post.date }}</div>
        {% endif %}
        <div class="title" style="font-weight: 500;">
            <a href="{{ post.url }}" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='#FF7900'" onmouseout="this.style.color='inherit'">
                {{ post.title }}
                <span class="external-icon" style="font-size: 0.75em; margin-left: 4px; opacity: 0.3; vertical-align: middle;">↗</span>
            </a>
        </div>
    </div>
    {% endfor %}
</div>
