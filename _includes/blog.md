<h2 id="blog" style="margin: 60px 0px 15px;">Blog</h2>

<div class="blog-container" style="display: flex; flex-direction: column; gap: 8px;">
    <!-- Internal Posts -->
    <!-- {% for post in site.posts %} -->
    <!-- <div class="blog-post" style="display: flex; align-items: baseline; font-size: 0.95em;">
        <div class="date" style="color: #999; width: 65px; flex-shrink: 0; font-size: 0.9em;">{{ post.date | date: "%Y.%m" }}</div>
        <div class="title-container" style="display: flex; flex-direction: column;">
            <div class="title" style="font-weight: 500;">
                <a href="{{ post.url | relative_url }}" style="color: inherit; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='#FF7900'" onmouseout="this.style.color='inherit'">
                    {{ post.title }}
                </a>
            </div>
            {% if post.tldr %}
            <div class="excerpt" style="font-size: 0.85em; color: #777; margin-top: 2px; line-height: 1.4;">{{ post.tldr | truncate: 150 }}</div>
            {% endif %}
        </div>
    </div> -->
    <!-- {% endfor %} -->

    <!-- {% if site.posts.size > 0 and site.data.blog.size > 0 %}
    <hr style="border: 0; height: 1px; background: #eee; margin: 15px 0;">
    {% endif %} -->

    <!-- External Links (from blog.yml) -->
    {% for post in site.data.blog %}
    <div class="blog-post" style="display: flex; align-items: baseline; font-size: 0.95em;">
        <div class="date" style="color: #999; width: 65px; flex-shrink: 0; font-size: 0.9em;">{{ post.date }}</div>
        <div class="title-container" style="display: flex; flex-direction: column;">
            <div class="title" style="font-weight: 500;">
                <a href="{{ post.url }}" target="_blank" rel="noopener noreferrer" style="color: inherit; text-decoration: none; transition: color 0.2s ease;" onmouseover="this.style.color='#FF7900'" onmouseout="this.style.color='inherit'">
                    {{ post.title }}
                    <span class="external-icon" style="font-size: 0.75em; margin-left: 4px; opacity: 0.3; vertical-align: middle;">↗</span>
                </a>
                {% if post.tag %}
                <span style="font-size: 0.9em; font-weight: 400; font-style: italic; color: #999; margin-left: 6px;">#{{ post.tag }}</span>
                {% endif %}
            </div>
            <!-- {% if post.description %}
            <div class="excerpt" style="font-size: 0.85em; color: #777; margin-top: 2px; line-height: 1.4;">{{ post.description }}</div>
            {% endif %} -->
        </div>
    </div>
    {% endfor %}
</div>
