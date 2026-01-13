<div class="news">
  <h2>News</h2>
  {% if site.data.news %}
    <div class="table-responsive">
      <table class="table table-sm table-borderless">
      {% for item in site.data.news %}
        <tr>
          <th scope="row" style="color: #333;">{{ item.date }}</th>
          <td>
            {% if item.inline %}
              <span style="color: #333;">{{ item.content | remove: '<p>' | remove: '</p>' | emojify }}</span>
            {% else %}
              <a class="news-title" href="{{ item.url | relative_url }}">{{ item.title }}</a>
            {% endif %}
          </td>
        </tr>
      {% endfor %}
      </table>
    </div>
  {% else %}
    <p>No news so far...</p>
  {% endif %}
</div>
