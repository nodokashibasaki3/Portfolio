<style>
  .hobby-container {
    display: flex;
    gap: 24px;
    margin-top: 35px;
    margin-bottom: 30px;
    align-items: center;
    font-size: 0.9em;
  }
  .hobby-item {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: inherit;
    cursor: default;
    position: relative;
  }
  .hobby-item.link-item {
    cursor: pointer;
  }
  .hobby-emoji {
    font-size: 1.2em;
    transition: transform 0.2s ease;
    filter: grayscale(0.2);
  }
  .hobby-label {
    max-width: 0;
    overflow: hidden;
    white-space: nowrap;
    opacity: 0;
    transition: max-width 0.4s ease, opacity 0.3s ease, margin-left 0.3s ease;
    font-size: 0.95em;
    color: #666;
    margin-left: 0;
  }
  .external-icon {
    font-size: 0.7em;
    margin-left: 4px;
    opacity: 0.5;
    vertical-align: super;
  }
  .hobby-item:hover .hobby-emoji {
    transform: scale(1.1);
    filter: grayscale(0);
  }
  .hobby-item:hover .hobby-label {
    max-width: 300px;
    opacity: 1;
    margin-left: 8px;
  }
</style>

<div class="hobby-container">
  <span style="color: #999; font-size: 0.85em; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-right: -8px;">Writing & Interests:</span>

  <a class="hobby-item link-item" href="https://nodokas.notion.site/Tokyo-Food-Review-2d3f432196de817b8033f41e42cf33ac" target="_blank" title="Read Food Blog">
    <span class="hobby-emoji">😋</span>
    <span class="hobby-label">Food Reviews <span class="external-icon">↗</span></span>
  </a>
  
  <a class="hobby-item link-item" href="https://nodokas.notion.site/macOS-Optimization-30ef432196de80b287f2e297420d1d46?source=copy_link" target="_blank" title="Read MacOS Blog">
    <span class="hobby-emoji">💻</span>
    <span class="hobby-label">macOS Optimization <span class="external-icon">↗</span></span>
  </a>

  <a class="hobby-item link-item" href="https://nodokas.notion.site/macOS-Optimization-and-Shell-Tools-30ef432196de80b287f2e297420d1d46?source=copy_link" target="_blank" title="Read OS Contribution Blog">
    <span class="hobby-emoji">🌐</span>
    <span class="hobby-label">OS Contribution <span class="external-icon">↗</span></span>
  </a>

  <div class="hobby-item">
    <span class="hobby-emoji">🏀</span>
    <span class="hobby-label">Basketball, Running</span>
  </div>
</div>
